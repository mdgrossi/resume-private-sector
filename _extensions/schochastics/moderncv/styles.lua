function Header(el)
    if level == 1 then
        local cv = pandoc.RawInline('latex', '\\section{' .. pandoc.utils.stringify(el.content) .. '} \\vspace{4pt}')
    end
    if level == 2 then
        local cv = pandoc.RawInline('latex', '\\subsection{' .. pandoc.utils.stringify(el.content) .. '} \\vspace{4pt}')
    end
    return cv
end
