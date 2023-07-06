C $Header$
C $Name$

#ifdef ALLOW_GUD

CBOP
C    !ROUTINE: GUD_SIZE.h
C    !INTERFACE:
C #include GUD_SIZE.h

C    !DESCRIPTION:
C Contains dimensions and index ranges for cell model.

      integer nplank, nGroup, nlam, nopt
      integer nPhoto
      integer iMinBact, iMaxBact
      integer iMinPrey, iMaxPrey
      integer iMinPred, iMaxPred
      integer nChl
      integer nPPplank
      integer nGRplank
      parameter(nlam=1)
      parameter(nopt=1)
      parameter(nplank=3)
      parameter(nGroup=13)
C  There are 2 photo      
      parameter(nPhoto=2)
C Weirdness is to turn off Bact max less than min will skip loop, the other are hardcoded to remove bact ref      
      parameter(iMinBact=1, iMaxBact=0)
      parameter(iMinPrey=1, iMaxPrey=2)
      parameter(iMinPred=3, iMaxPred=3)
      parameter(nChl=0)
      parameter(nPPplank=0)
      parameter(nGRplank=0)

CEOP
#endif /* ALLOW_GUD */
