# =============================================================================
#
# HTML Rendering
# From https://github.com/busemorose/resume_quarto
#
# =============================================================================

rmlatex <- function(string){
  
  # Remove commands
  string <- trimws(gsub("\\\\v.*}", "", string))
  string <- trimws(gsub("\\\\h.*}", "", string))
  string <- trimws(gsub("\\\\t.*}", "", string))
  
  # Remove escape characters
  string <- trimws(gsub("\\\\", "", string))

  # Replace * with bullets
  string <- gsub("[*]", "\u2022", string)

  # Replace other odds and ends
  string <- gsub("[$]sim[$]", "~", string)
  string <- gsub("[$]>[$]", ">", string)

  return(string)
}

html.skillbars <- function(df, fontsize=20){
  # Create and clear dataframe
  df <- as.data.frame(df)
  df <- df %>% dplyr::mutate_all(rmlatex)
  df$label = paste(df$skill, df$years, sep=": ")
  
  # Expand data table for two-color bars
  dat <- rbind(
    transform(df, type=1, fill = "#3873b3"),
    transform(df, type=2, scale=1-as.numeric(scale), fill="lightgrey")
  )
  
  # Create plot
  ggplot(data=dat, aes(x=skill, y=as.numeric(scale), fill=fill)) +
    geom_bar(stat="identity", position=position_fill(reverse=TRUE), width=0.75) +
    facet_wrap(~label, scales="free_y") +
    scale_fill_identity(guide="none") +
    labs(x=NULL, y=NULL) + 
    scale_y_continuous(expand=c(0,0)) +
    scale_x_discrete(expand=c(0,0)) +
    coord_flip() +
    theme_classic() +
    theme(axis.ticks.y=element_blank(),
          axis.ticks.x=element_blank(),
          axis.text.y=element_blank(),
          axis.text.x=element_blank(),
          axis.line=element_blank(),
          strip.text = element_text(size = fontsize),
          strip.background = element_blank(),
          plot.margin=unit(c(10,10,10,10),"mm")
          )
    # geom_chicklet(radius = grid::unit(3, 'mm')) +
    # annotate("text", y=0.3, x=1, label=df$label, color="white", size=10) +
}


html.cvsoftskills <- function(skills) {

    cat(paste0("**Soft Skills:** ", skills))
}

exp_pro <- function(tbl, employer, job, date, where, desc) {
  
  # De-LaTeXify
  tbl <- tbl %>% dplyr::mutate_all(rmlatex)
  tbl[tbl == ""] <- " "

  # List for adding subtitle
  new_row <- list()
  jobcity <- paste(tbl[[job]], tbl[[where]], sep=", ")
  new_row[[tbl[[employer]]]] = jobcity
  new_row[[" "]] = tbl[[date]]
  
  # List for content
  if(tbl[[employer]] == " "){
        tbl[[employer]] = "   "
  }
  new_content <- list()
  new_content[[tbl[[employer]]]] = tbl[[desc]]
  new_content[[" "]] = tbl[[desc]]
  
  tibble(!!tbl[[employer]] := NA, !!" " := NA) |> 
    flextable() |>
    set_table_properties(layout = "autofit", width = 1) |>
    # Add job and city variable as subtitle
    add_header(values = new_row,
               top = FALSE) |>
    # Add content
    add_body(values = new_content) |> 
    # Bold employer
    compose(part = "header",
            i = 1, j = 1,
            value = as_paragraph(as_b(tbl[[employer]]))) |> 
    # Italic job
    compose(part = "header",
            i = 2, j = 1,
            value = as_paragraph(as_i(jobcity))) |> 
    # Italic city
    compose(part = "header",
            i = 2, j = 2,
            value = as_paragraph(as_i(tbl[[date]]))) |> 
    # Merge
    merge_h() |>
    # Remove padding of all table
    padding(part = "all", padding = 1) |> 
    # Add padding under header section
    padding(i = 2, padding.bottom = 10, part = "header") |> 
    # Remove borders
    border_remove() |>
    align(part = "all", align = "left") |>
    align(part = "all", j = 2, align = "right") |>  
    font(part = "all", fontname = "Lato") |>
    color(part = "all", color = "#212529") |> 
    fontsize(size = 14, part = "header") |>
    fontsize(size = 13.5, part = "body") |>
    line_spacing(space = 1.5, part = "all")
}

exp_school <- function(degree, year, school, city) {
  
  # List for content
  new_content <- list()
  new_content[[degree]] = school[1:length(school)]
  new_content[[year]] = city
  
  tibble(!!degree := NA, !!year := NA) |> 
    flextable() |>
    set_table_properties(layout = "autofit", width = 1) |>
    # Add content
    add_body(values = new_content) |>
    # Bold degree
    compose(part = "header",
            i = 1, j = 1,
            value = as_paragraph(as_b(degree))) |> 
    # Italic school
    compose(part = "body",
            i = 1, j = 1,
            value = as_paragraph(as_i(school))) |>
    # Italic location
    compose(part = "body",
            i = 1, j = 2,
            value = as_paragraph(as_i(city))) |>     # Merge
    merge_h() |>
    # Remove padding of all table
    padding(part = "all", padding = 1) |> 
    # Add padding under header section
    padding(i = 1, padding.bottom = 10, part = "header") |> 
    # Remove borders
    border_remove() |>
    align(part = "all", align = "left") |>
    align(part = "all", j = 2, align = "right") |>  
    font(part = "all", fontname = "Lato") |>
    color(part = "all", color = "#212529") |> 
    fontsize(size = 14, part = "header") |>
    fontsize(size = 13.5, part = "body")
}