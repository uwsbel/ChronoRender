# M.Kesson Dec 2010, modified Sept 2011
proc saveJPG { name { gamma 2.2 } { quality 100} } {
    set path [file join [pwd] $name]    
    set cat [it GetCurrentCatalog]
    set img [$cat GetCurrentImage]
    set handle [$img GetHandle]
    ::RAT::LogMsg NOTICE "saving image to \"$path\""

    it IceExpr "result := $handle Gamma($gamma)"    
    set expression "result SetMetaDataItem(\"JPEG_QUALITY\", $quality) ; "
    append expression "result Save(\"$path\", IceOutputType Jpeg)"
    it IceExpr $expression

    $cat DeleteImage [$cat GetCurrentImage]
}
