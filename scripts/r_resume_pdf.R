# =============================================================================
#
# Functions for PDF rendering
#
# =============================================================================

cvskills <- function(tbl, skill, years, scale, cols) {

    colscall <- paste0(
      "\\vspace{-1em}", "\\begin{multicols}", "{", cols, "}"
    )
    command_start <- "\\cvskillbar"
    res <- paste0(
      command_start, "{", tbl[[skill]], "}",
      "{", tbl[[years]], "}",
      "{", as.numeric(tbl[[scale]]), "}"
    )
    colsend <- "\\end{multicols}"
    cat(colscall, res, colsend, sep = "\n")
}

cvsoftskills <- function(skills) {

    command_start <- paste0("\\cvitem{\\textcolor{color1}{$\\triangleright$} \\hspace{0.2em} Soft Skills}")
    command_end <- "\\vspace{\\cvspace}"
    res <- paste0(command_start, "{", skills, "}")

    cat(res)
    cat(command_end)
}

cvevents <- function(tbl, when, what, where, city, descr) {

    command_start <- "\\cventry[\\cvspace]"
    # tbl[[where]] <- gsub("\n", " \\\\newline ", tbl[[where]])
    tbl[[descr]] <- gsub("* ", "\\item ", tbl[[descr]], fixed=TRUE)
    res <- paste0(
        command_start, "{", tbl[[when]], "}", 
        "{", tbl[[what]], "}",
        "{", tbl[[where]], "}",
        "{}",
        "{", tbl[[city]], "}",
        "{", "\\vspace{0.25em}\\begin{wideitemize}", tbl[[descr]], "\\end{wideitemize}", "}",
        "\\vspace{0.5em}"
        )

    cat(res, sep = "\n\n\n")
}

cvedu <- function(tbl, where, institution, degree, when, extra1=NA, extra2=NA) {

    command_start <- "\\cventry"
    res <- paste0(
        command_start, "{", tbl[[where]], "}", 
        "{", tbl[[institution]], "}",
        "{", tbl[[degree]], "}",
        "{", tbl[[when]], "}",
        "{", tbl[[extra1]], "}",
        "{", tbl[[extra2]], "}",
        )

    cat(res, sep = "\n\n\n")
}

cvaward <- function(tbl, award){

    res <- paste0(
        "\\cvlistitem", "{", tbl[[award]], "}"
    )

    cat(res, sep = "\n\n\n")
}