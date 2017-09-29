ROOTTEST_GENERATE_DICTIONARY(systemModulemapDict systemModulemap.h LINKDEF systemModulemapLinkdef.h)

#ROOTTEST_ADD_TEST(systemModulemap
#                  MACRO systemModulemap.C
#                  OUTREF systemModulemap.ref
#                  DEPENDS systemModulemap-build
#                  LABELS roottest cling)
