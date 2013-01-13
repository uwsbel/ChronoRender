############################ Types ###################################

RtBoolean = bool
RtInt = int
RtFloat = float
RtString = str
RtToken = str
RtVoid = None
RtPointer = lambda x: x

RtColor = tuple
RtPoint = tuple
RtVector = tuple
RtNormal = tuple
RtHpoint = tuple
RtMatrix = tuple
RtBasis = tuple
RtBound = tuple

RtObjectHandle = lambda x: x
RtLightHandle = lambda x: x
RtContextHandle = lambda x: x

RtFilterFunc = lambda x: x
RtErrorHandler = lambda x: x
RtProcSubdivFunc = lambda x: x
RtProcFreeFunc = lambda x: x
RtArchiveCallback = lambda x: x
