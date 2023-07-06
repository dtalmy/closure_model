C $Header$
C $Name$

#include "GUD_OPTIONS.h"

CBOP
C !ROUTINE: GUD_MODEL
C !INTERFACE: ==========================================================
      SUBROUTINE GUD_GRAZING(
     I     Ptr,
     U     gTr,
     U     diags,
     I     grazTempFunc, reminTempFunc, mortTempFunc, mort2TempFunc,
     I     myTime,myIter,myThid)

C !DESCRIPTION:
C     add quota-style grazing tendencies to gPtr

C !USES: ===============================================================
      IMPLICIT NONE
#include "GUD_SIZE.h"
#include "GUD_INDICES.h"
#include "GUD_DIAGS.h"
#include "GUD_GENPARAMS.h"
#include "GUD_TRAITS.h"

C !INPUT PARAMETERS: ===================================================
C  Ptr    :: gud model tracers
C  Temp   :: temperature field (degrees C)
C  myTime :: current time
C  myIter :: current iteration number
C  myThid :: thread number
      _RL Ptr(nGud)
      _RL grazTempFunc(nplank)
      _RL mortTempFunc
      _RL mort2TempFunc
      _RL reminTempFunc
      INTEGER myThid, myIter
      _RL myTime

C !INPUT/OUTPUT PARAMETERS: ============================================
C  gTr    :: accumulates computed tendencies
C  diags  :: accumulates diagnostics
      _RL gTr(nGud)
      _RL diags(gud_nDiag)
CEOP

#ifdef ALLOW_GUD

c !LOCAL VARIABLES: ====================================================
      INTEGER jz, jp

      _RL Qc  (nplank)
      _RL Qn  (nplank)
      _RL Qp  (nplank)
      _RL Qsi (nplank)
      _RL Qfe (nplank)
      _RL QChl(nChl)
      _RL X   (nplank)
      _RL Xi  (nplank)

      _RL regQc, regQn, regQp, regQfe
      _RL sumprey, sumpref, grazphy

      _RL preygraz   (nplank)
      _RL predgrazc  (nplank)
      _RL predgrazn  (nplank)
      _RL predgrazp  (nplank)
      _RL predgrazfe (nplank)

      _RL totkillc, totkilln, totkillp, totkillsi, totkillfe
#ifdef GUD_ALLOW_CARBON
      _RL totkillPIC
#endif
      _RL totkillexpc, totkillexpn, totkillexpp, totkillexpfe
      _RL predexpc, predexpn, predexpp, predexpfe
      _RL graz2OC, graz2ON, graz2OP, graz2OFe
      _RL graz2POC, graz2PON, graz2POP, graz2POSi, graz2POFe
      _RL graz2PIC

      _RL tmp, expfrac

      _RL Xe
      _RL mortX
      _RL mortX2

      _RL lasseffC
      _RL lasseffN
      _RL lasseffP
      _RL lasseffFe
 
      _RL lexpFrac

      _RL exude_DOC
      _RL exude_DON
      _RL exude_DOP
      _RL exude_DOFe

      _RL exude_PIC
      _RL exude_POC
      _RL exude_PON
      _RL exude_POP
      _RL exude_POSi
      _RL exude_POFe

      _RL mort_c(nplank)

      _RL respir
      _RL respir_c

#ifdef GUD_ALLOW_CDOM
      _RL graz2CDOM, exude_CDOM
#endif

      _RL EPS
      PARAMETER (EPS=1D-38)

C==== make all bio fields non-negative and compute quotas ==============

C fixed carbon quota, for now 1.0 (may change later)
      Qc(:) = 1.0
      X(:) = MAX(0., Ptr(ic:ec))/Qc(:)
C other elements: get quota from corresponding ptracer or set to fixed
c ratio if not variable.
      Xi(:) = 1.0 _d 0/MAX(EPS, X(:))
#ifdef GUD_ALLOW_NQUOTA
      Qn(:) = MAX(0., Ptr(in:en))*Xi(:)
#else
      Qn(:) = R_NC(:)
#endif
#ifdef GUD_ALLOW_PQUOTA
      Qp(:) = MAX(0., Ptr(ip:ep))*Xi(:)
#else
      Qp(:) = R_PC(:)
#endif
#ifdef GUD_ALLOW_SIQUOTA
      Qsi(:) = MAX(0., Ptr(isi:esi))*Xi(:)
#else
      Qsi(:) = R_SiC(:)
#endif
#ifdef GUD_ALLOW_FEQUOTA
      Qfe(:) = MAX(0., Ptr(ife:efe))*Xi(:)
#else
      Qfe(:) = R_FeC(:)
#endif
#ifdef GUD_ALLOW_CHLQUOTA
      QChl(:) = MAX(0., Ptr(ichl:echl))*Xi(1:nChl)
#endif

      preygraz(:)   = 0.0
      predgrazc(:)  = 0.0
      predgrazn(:)  = 0.0
      predgrazp(:)  = 0.0
      predgrazfe(:) = 0.0
      
      graz2POC  = 0.0
      graz2PON  = 0.0
      graz2POP  = 0.0
      graz2POSI = 0.0
      graz2POFE = 0.0
      graz2OC   = 0.0
      graz2ON   = 0.0
      graz2OP   = 0.0
      graz2OFE  = 0.0
      graz2PIC  = 0.0

      regQn  = 1.0
      regQp  = 1.0
      regQfe = 1.0
      regQc  = 1.0

C=======================================================================
      DO jz = iMinPred, iMaxPred

C       regulate grazing near full quota
        regQc = 1.0 _d 0
#ifdef GUD_ALLOW_NQUOTA
        regQn = 1. _d 0
#endif
#ifdef GUD_ALLOW_PQUOTA
        regQp = 1. _d 0
#endif
#ifdef GUD_ALLOW_FEQUOTA
        regQfe = 1. _d 0
#endif


        sumprey = 0.0
        sumpref = 0.0
        DO jp = iMinPrey, iMaxPrey
         sumprey = sumprey + palat(jp,jz)*X(jp)
#ifdef GUD_GRAZING_SWITCH
         sumpref=sumpref+palat(jp,jz)*palat(jp,jz)*X(jp)*X(jp)
#else
         sumpref=sumpref + palat(jp,jz)*X(jp)
#endif
        ENDDO
        sumprey = MAX(0.0, sumprey - phygrazmin)
        sumpref = MAX(phygrazmin, sumpref)
        tmp = grazemax(jz)*grazTempFunc(jz)*X(jz)*
     &    (sumprey**hollexp/(sumprey**hollexp+kgrazesat(jz)**hollexp))*
     &    (1.0 - EXP(-inhib_graz*sumprey))**inhib_graz_exp

        totkillc  = 0.0 _d 0
        totkilln  = 0.0 _d 0
        totkillp  = 0.0 _d 0
        totkillsi = 0.0 _d 0
        totkillfe = 0.0 _d 0
#ifdef GUD_ALLOW_CARBON
        totkillPIC= 0.0 _d 0
#endif
        totkillexpc  = 0.0 _d 0
        totkillexpn  = 0.0 _d 0
        totkillexpp  = 0.0 _d 0
        totkillexpfe = 0.0 _d 0
        predexpc  = 0.0 _d 0
        predexpn  = 0.0 _d 0
        predexpp  = 0.0 _d 0
        predexpfe = 0.0 _d 0
        DO jp = iMinPrey, iMaxPrey

          IF (isVir(jz) .EQ. 0) THEN
            lasseffC  = 0.3
            lasseffN  = 0.3
            lasseffP  = 0.3
            lasseffFe = 0.3
            lexpFrac = 1.0
          ELSE
            lasseffC  = 0.05
            lasseffN  = 0.05
            lasseffP  = 0.05
            lasseffFe = 0.05
            lexpFrac = 1.0
          ENDIF

#ifdef GUD_GRAZING_SWITCH
          grazphy = tmp*palat(jp,jz)*palat(jp,jz)*X(jp)*X(jp)/sumpref
#else
          grazphy = tmp*palat(jp,jz)*X(jp)/sumpref
#endif

          preygraz(jp) = preygraz(jp) + grazphy

          totkillc  = totkillc  + grazphy
          totkilln  = totkilln  + grazphy*Qn (jp)
          totkillp  = totkillp  + grazphy*Qp (jp)
          totkillsi = totkillsi + grazphy*Qsi(jp)
          totkillfe = totkillfe + grazphy*Qfe(jp)
#ifdef GUD_ALLOW_CARBON
          totkillPIC= totkillPIC+ grazphy*R_PICPOC(jp)
#endif

!         for now, use locally defined expFrac to distinguish
!         grazers and viruses      
!         expFrac = ExportFracPreyPred(jp,jz)
          totkillexpc  = totkillexpc  + lexpFrac*grazphy
          totkillexpn  = totkillexpn  + lexpFrac*grazphy*Qn (jp)
          totkillexpp  = totkillexpp  + lexpFrac*grazphy*Qp (jp)
          totkillexpfe = totkillexpfe + lexpFrac*grazphy*Qfe(jp)

          predgrazc(jz) = predgrazc(jz) + grazphy*lasseffC*regQc
          predexpc = predexpc + lexpFrac*grazphy*lasseffC*regQc
#ifdef GUD_ALLOW_NQUOTA
          predgrazn(jz) = predgrazn(jz) + grazphy*lasseffN*
     &                                    regQn*Qn(jp)
          predexpn = predexpn + lexpFrac*grazphy*lasseffN*
     &                                    regQn*Qn(jp)
#else
          predgrazn(jz) = predgrazn(jz) + grazphy*lasseffN*regQn
          predexpn = predexpn + lexpFrac*grazphy*lasseffN*regQn
#endif
#ifdef GUD_ALLOW_PQUOTA
          predgrazp(jz) = predgrazp(jz) + grazphy*lasseffP*
     &                                    regQp*Qp(jp)
          predexpp = predexpp + lexpFrac*grazphy*lasseffP*
     &                                  regQp*Qp(jp)
#else
          predgrazp(jz) = predgrazp(jz) + grazphy*lasseffP*regQp
          predexpp = predexpp + lexpFrac*grazphy*lasseffP*regQp
#endif

#endif
#ifdef GUD_ALLOW_FEQUOTA
          predgrazfe(jz) = predgrazfe(jz) + grazphy*lasseffFe*
     &                                      regQfe*Qfe(jp)
          predexpfe = predexpfe + lexpFrac*grazphy*lasseffFe*
     &                                    regQfe*Qfe(jp)
#else
          predgrazfe(jz) = predgrazfe(jz) + grazphy*lasseffFe*regQfe
          predexpfe = predexpfe + lexpFrac*grazphy*lasseffFe*regQfe
#endif
        ENDDO

        graz2OC   = graz2OC   + totkillc    - predgrazc(jz)
        graz2POC  = graz2POC  + totkillexpc - predexpc

#ifdef GUD_ALLOW_NQUOTA
        graz2ON   = graz2ON   + totkilln    - predgrazn(jz)
        graz2PON  = graz2PON  + totkillexpn - predexpn
#else
        graz2ON   = graz2ON   + totkilln    - predgrazn(jz)*Qn(jz)
        graz2PON  = graz2PON  + totkillexpn - predexpn     *Qn(jz)
#endif

#ifdef GUD_ALLOW_PQUOTA
        graz2OP   = graz2OP   + totkillp    - predgrazp(jz)
        graz2POP  = graz2POP  + totkillexpp - predexpp
#else
        graz2OP   = graz2OP   + totkillp    - predgrazp(jz)*Qp(jz)
        graz2POP  = graz2POP  + totkillexpp - predexpp     *Qp(jz)
#endif

#ifdef GUD_ALLOW_FEQUOTA
        graz2OFe  = graz2OFe   + totkillfe    - predgrazfe(jz)
        graz2POFe = graz2POFe  + totkillexpfe - predexpfe
#else
        graz2OFe  = graz2OFe   + totkillfe    - predgrazfe(jz)*Qfe(jz)
        graz2POFe = graz2POFe  + totkillexpfe - predexpfe     *Qfe(jz)
#endif

        graz2POSi = graz2POSi + totkillsi

#ifdef GUD_ALLOW_CARBON
        graz2PIC  = graz2PIC  + totkillPIC
#endif

C     end predator loop
      ENDDO

C==== tendencies =======================================================

      gTr(iDOC )=gTr(iDOC ) + graz2OC  - graz2POC
      gTr(iDON )=gTr(iDON ) + graz2ON  - graz2PON
      gTr(iDOP )=gTr(iDOP ) + graz2OP  - graz2POP
      gTr(iDOFe)=gTr(iDOFe) + graz2OFe - graz2POFe
      gTr(iPOC )=gTr(iPOC ) + graz2POC
      gTr(iPON )=gTr(iPON ) + graz2PON
      gTr(iPOP )=gTr(iPOP ) + graz2POP
      gTr(iPOSi)=gTr(iPOSi) + graz2POSi
      gTr(iPOFe)=gTr(iPOFe) + graz2POFe
#ifdef GUD_ALLOW_CARBON
      gTr(iPIC )=gTr(iPIC ) + graz2PIC
#endif
#ifdef GUD_ALLOW_CDOM
      graz2CDOM = fracCDOM*(graz2OP - graz2POP)
      gTr(iCDOM)=gTr(iCDOM) + graz2CDOM
      gTr(iDOC )=gTr(iDOC )             - R_CP_CDOM*graz2CDOM
      gTr(iDON )=gTr(iDON )             - R_NP_CDOM*graz2CDOM
      gTr(iDOP )=gTr(iDOP ) - graz2CDOM
      gTr(iDOFe)=gTr(iDOFe)             - R_FeP_CDOM*graz2CDOM
#endif
      DO jp = iMinPrey, iMaxPrey
       gTr(ic+jp-1)= gTr(ic+jp-1) - preygraz(jp)
      ENDDO
      DO jz = iMinPred, iMaxPred
       gTr(ic+jz-1)=gTr(ic+jz-1) + predgrazc(jz)
      ENDDO
#ifdef GUD_ALLOW_NQUOTA
      gTr(in:en)=gTr(in:en) + predgrazn(:) - preygraz(:)*Qn(:)
#endif
#ifdef GUD_ALLOW_PQUOTA
      gTr(ip:ep)=gTr(ip:ep) + predgrazp(:) - preygraz(:)*Qp(:)
#endif
#ifdef GUD_ALLOW_SIQUOTA
      gTr(isi:esi)=gTr(isi:esi) - preygraz(:)*Qsi(:)
#endif
#ifdef GUD_ALLOW_FEQUOTA
      gTr(ife:efe)=gTr(ife:efe) + predgrazfe(:) - preygraz(:)*Qfe(:)
#endif
#ifdef GUD_ALLOW_CHLQUOTA
      gTr(iChl:eChl)=gTr(iChl:eChl) - preygraz(1:nChl)*QChl(:)
#endif

      DO jp = 1, nGRplank
        diags(iGRplank+jp-1) = preygraz(jp)
      ENDDO

C==== mortality ========================================================
      exude_DOC  = 0.0 _d 0
      exude_POC  = 0.0 _d 0
      exude_DON  = 0.0 _d 0
      exude_PON  = 0.0 _d 0
      exude_DOFe = 0.0 _d 0
      exude_POFe = 0.0 _d 0
      exude_DOP  = 0.0 _d 0
      exude_POP  = 0.0 _d 0
      exude_POSi = 0.0 _d 0
      exude_PIC  = 0.0 _d 0
      respir     = 0.0 _d 0

      DO jp = 1, nplank
        Xe = MAX(0 _d 0, X(jp) - Xmin(jp))
        mortX = mort(jp)*Xe*MAX(mortTempFuncMin(jp), mortTempFunc)
        mortX2= mort2(jp)*Xe*Xe*MAX(mort2TempFuncMin(jp), mort2TempFunc)

        mort_c(jp) = mortX + mortX2

        exude_DOC = exude_DOC + (1.-ExportFracMort(jp)) *mortX
     &                        + (1.-ExportFracMort2(jp))*mortX2
        exude_POC = exude_POC +     ExportFracMort(jp)  *mortX
     &                        +     ExportFracMort2(jp) *mortX2

        exude_DON = exude_DON + (1.-ExportFracMort(jp)) *mortX *Qn(jp)
     &                        + (1.-ExportFracMort2(jp))*mortX2*Qn(jp)
        exude_PON = exude_PON +     ExportFracMort(jp)  *mortX *Qn(jp)
     &                        +     ExportFracMort2(jp) *mortX2*Qn(jp)

        exude_DOP = exude_DOP + (1.-ExportFracMort(jp)) *mortX *Qp(jp)
     &                        + (1.-ExportFracMort2(jp))*mortX2*Qp(jp)
        exude_POP = exude_POP +     ExportFracMort(jp)  *mortX *Qp(jp)
     &                        +     ExportFracMort2(jp) *mortX2*Qp(jp)

        exude_DOFe= exude_DOFe+ (1.-ExportFracMort(jp)) *mortX *Qfe(jp)
     &                        + (1.-ExportFracMort2(jp))*mortX2*Qfe(jp)
        exude_POFe= exude_POFe+     ExportFracMort(jp)  *mortX *Qfe(jp)
     &                        +     ExportFracMort2(jp) *mortX2*Qfe(jp)

        exude_POSi = exude_POSi + mort_c(jp)*Qsi(jp)

        exude_PIC = exude_PIC + mort_c(jp)*R_PICPOC(jp)

        respir_c = respiration(jp)*Xe*reminTempFunc
        respir = respir + respir_c

        gTr(ic+jp-1)=gTr(ic+jp-1)  - mort_c(jp) - respir_c
#ifdef GUD_ALLOW_NQUOTA
        gTr(in+jp-1)=gTr(in+jp-1)  - mort_c(jp)*Qn(jp)
#endif
#ifdef GUD_ALLOW_PQUOTA
        gTr(ip+jp-1)=gTr(ip+jp-1)  - mort_c(jp)*Qp(jp)
#endif
#ifdef GUD_ALLOW_SIQUOTA
        gTr(isi+jp-1)=gTr(isi+jp-1) - mort_c(jp)*Qsi(jp)
#endif
#ifdef GUD_ALLOW_FEQUOTA
        gTr(ife+jp-1)=gTr(ife+jp-1) - mort_c(jp)*Qfe(jp)
#endif

#ifdef GUD_ALLOW_EXUDE
        exude_DOC = exude_DOC + (1.-ExportFrac(jp))*kexcC(jp)*Xe
        exude_POC = exude_POC +     ExportFrac(jp) *kexcC(jp)*Xe
        exude_DON = exude_DON + (1.-ExportFrac(jp))*kexcN(jp)*Xe*Qn(jp)
        exude_PON = exude_PON +     ExportFrac(jp) *kexcN(jp)*Xe*Qn(jp)
        exude_DOP = exude_DOP + (1.-ExportFrac(jp))*kexcP(jp)*Xe*Qp(jp)
        exude_POP = exude_POP +     ExportFrac(jp) *kexcP(jp)*Xe*Qp(jp)
        exude_DOFe=exude_DOFe+(1.-ExportFrac(jp))*kexcFe(jp)*Xe*Qfe(jp)
        exude_POFe=exude_POFe+    ExportFrac(jp) *kexcFe(jp)*Xe*Qfe(jp)
        exude_POSi = exude_POSi + kexcSi(jp)*Xe*Qsi(jp)
        gTr(ic+jp-1)=gTr(ic+jp-1)   - kexcC(jp)*Xe
#ifdef GUD_ALLOW_NQUOTA
        gTr(in+jp-1)=gTr(in+jp-1)   - kexcN(jp)*Xe*Qn(jp)
#endif
#ifdef GUD_ALLOW_PQUOTA
        gTr(ip+jp-1)=gTr(ip+jp-1)   - kexcP(jp)*Xe*Qp(jp)
#endif
#ifdef GUD_ALLOW_SIQUOTA
        gTr(isi+jp-1)=gTr(isi+jp-1) - kexcSi(jp)*Xe*Qsi(jp)
#endif
#ifdef GUD_ALLOW_FEQUOTA
        gTr(ife+jp-1)=gTr(ife+jp-1) - kexcFe(jp)*Xe*Qfe(jp)
#endif
#endif
      ENDDO

#ifdef GUD_ALLOW_CHLQUOTA
      DO jp = 1, nChl
        gTr(iChl+jp-1)=gTr(iChl+jp-1) - mort_c(jp)*QChl(jp)
      ENDDO
#endif

      gTr(iDIC )=gTr(iDIC ) + respir

      gTr(iDOC )=gTr(iDOC ) + exude_DOC
      gTr(iDON )=gTr(iDON ) + exude_DON
      gTr(iDOP )=gTr(iDOP ) + exude_DOP
      gTr(iDOFe)=gTr(iDOFe) + exude_DOFe

      gTr(iPIC )=gTr(iPIC ) + exude_PIC
      gTr(iPOC )=gTr(iPOC ) + exude_POC
      gTr(iPON )=gTr(iPON ) + exude_PON
      gTr(iPOP )=gTr(iPOP ) + exude_POP
      gTr(iPOSi)=gTr(iPOSi) + exude_POSi
      gTr(iPOFe)=gTr(iPOFe) + exude_POFe
#ifdef GUD_ALLOW_CDOM
      exude_CDOM = fracCDOM*exude_DOP
      gTr(iCDOM)=gTr(iCDOM) + exude_CDOM
      gTr(iDOC )=gTr(iDOC )              - R_CP_CDOM*exude_CDOM
      gTr(iDON )=gTr(iDON )              - R_NP_CDOM*exude_CDOM
      gTr(iDOP )=gTr(iDOP ) - exude_CDOM
      gTr(iDOFe)=gTr(iDOFe)              - R_FeP_CDOM*exude_CDOM
#endif
C 
C#endif /* ALLOW_GUD */

      RETURN
      END SUBROUTINE

