# Add --shell-escape flag needed for minted
$latex = 'latex  %O  --shell-escape %S';
#$pdflatex = 'pdflatex  %O  --shell-escape %S';
$pdflatex = 'lualatex -file-line-error %O --shell-escape %S';
$pdf_mode = 1;



ensure_path( 'TEXINPUTS', './estonian//' );
ensure_path( 'TEXINPUTS', './english//' );