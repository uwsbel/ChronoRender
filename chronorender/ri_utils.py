
def seq2col(seq):
    """Convert a sequence containing a color into a string."""
    if len(seq)<self._colorsamples:
        self._error(RIE_INVALIDSEQLEN, RIE_ERROR, "Invalid sequence length ("+\
               `len(seq)`+" instead of "+`self._colorsamples`+")")
    colseq = tuple(seq)
    return '['+string.join( map(lambda x: str(x), colseq[:self._colorsamples]) )+']'

def flatten(seq):
    """Return a list of the individual items in a (possibly nested) sequence.

    Returns a list with all items as strings.
    If an item was already a string it's enclosed in apostrophes.
    
    Example: _flatten( [(1,2,3), (4,5,6)] ) -> ["1","2","3","4","5","6"]
             _flatten( ("str1","str2") )    -> ['"str1"','"str2"']
    """
    res = []
    ScalarTypes = [types.IntType, types.LongType, types.FloatType]
    for v in seq:
        vtype = type(v)
        # v=scalar?
        if vtype in ScalarTypes:
            res.append(str(v))
        # vec3?
        # elif isinstance(v, _vec3):
            # res.extend([str(v.x), str(v.y), str(v.z)])
        # v=string?
        elif isinstance(v, basestring):
            res.append('"%s"'%v)
        # no scalar or string. Then it might be a sequence...
        else:
            # Check if it is really a sequence...
            try:
                n = len(v)
            except:
                res.append(str(v))
                continue
            res += flatten(v)
    return res

def seq2list(seq, count=None):
    """Convert a sequence into a string.

    The function checks if the sequence contains count elements (unless
    count is None). If it doesn't an error is generated.
    The return value is a string containing the sequence. The string can
    be used as parameter value to RIB commands.
    """

    f = flatten(seq)
    # Has the sequence an incorrect length? then generate an error
    if count!=None and len(f)!=count:
        self._error(RIE_INVALIDSEQLEN, RIE_ERROR, "Invalid sequence length ("+\
               `len(f)`+" instead of "+`count`+")")
        
    return '[%s]'%" ".join(f)

def paramlist2dict(paramlist, keyparams):
    """Combine the paramlists (tuple & dict) into one dict.
    
    paramlist is a tuple with function arguments (token/value pairs or
    a dictionary). keyparams is a dictionary with keyword arguments.
    The dictionary keyparams will be modified and returned.
    """

    if len(paramlist)==1 and type(paramlist[0])==types.DictType:
        keyparams = paramlist[0]
        paramlist = ()
    
    # Add the paramlist tuple to the keyword argument dict
    for i in range(len(paramlist)/2):
        token = paramlist[i*2]
        value = paramlist[i*2+1]
        keyparams[token]=value

    return keyparams

def paramlist2lut(paramlist, keyparams):
    """Combine the paramlists into one dict without inline declarations.

    paramlist is a tuple with function arguments. keyparams is a
    dictionary with keyword arguments. The dictionary keyparams will
    be modified and returned.

    The resulting dictionary can be used to look up the value of tokens.
    """
    # Add the paramlist tuple to the keyword argument dict
    for i in range(len(paramlist)/2):
        token = paramlist[i*2]
        value = paramlist[i*2+1]
        # Extract the name of the token (without inline declaration
        # if there is one)
        f = token.split(" ")
        tokname = f[-1]
        keyparams[tokname]=value

    return keyparams
    
def merge_paramlist(paramlist, keyparams):
    """Merge a paramlist tuple and keyparams dict into one single list.
    """
    if len(paramlist)==1 and type(paramlist[0])==types.DictType:
        keyparams = paramlist[0]
        paramlist = ()

    res = list(paramlist)
    # Check if the number of values is uneven (this is only allowed when
    # the last value is None (RI_NULL) in which case this last value is ignored)
    if (len(res)%2==1):
       if res[-1] is None:
           res = res[:-1]
       else:
           raise ValueError, "The parameter list must contain an even number of values" 

    # Append the params from the keyparams dict to the parameter list
    map(lambda param: res.extend(param), keyparams.iteritems())
    return res
    

def paramlist2string(paramlist, keyparams={}):
    """Convert the paramlist into a string representation.

    paramlist is a tuple with function arguments (token/value pairs or
    a dictionary). keyparams is a dictionary with keyword arguments.
    Each token has to be a string, the value can be of any type. If the
    value is a string, it's enclosed in apostrophes. A trailing token
    without a value is ignored, which also means that a trailing RI_NULL
    can be passed.
    The resulting string contains a leading space, unless there are no
    token/value pairs.
    """

    paramlist = merge_paramlist(paramlist, keyparams)

    res=""
    for i in range(0, len(paramlist), 2):
        token = paramlist[i].strip()
        value = paramlist[i+1]
        # Extract the name of the token (without inline declaration
        # if there is one)
        f = token.split(" ")
        tokname = f[-1:][0]
        inline  = f[:-1]

        if not (self._declarations.has_key(tokname) or inline!=[]):
            self._error(RIE_UNDECLARED,RIE_ERROR,'Parameter "'+tokname+
                   '" is not declared.')
        
        # Check if the value is a sequence (if it returns an iterator)
        isseq=0
        try:
            isseq = (iter(value)!=None)
        except:
            pass
        # Convert value into the appropriate string representation
        if isinstance(value, basestring):
            value='["'+value+'"]'
#        elif type(value)==types.ListType or type(value)==types.TupleType:
        elif isseq:
            value = seq2list(value)
        else:
            value='[%s]'%value
        res+=' "'+token+'" '+value

    if (res==" "): res=""
    return res
