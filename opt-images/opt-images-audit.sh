#!/bin/bash
#
# Definir permissões para o script:
# chmod u+x opt-images-audit.sh
#
# O arquivo deve ser executado no diretório de imagens.
# O script em awk não verifica arquivos sem extensão.
#
# Executar script remotamente:
# ssh user@host 'cd <PATH> && bash -s' < opt-images-audit.sh
#
# Versão: 0.1
# Autor: Claromes <claromes@celere.dev>

echo "-> Quantidade total de arquivos do diretório:" &&
ls -1 | wc -l &&
echo "-> Quantidade total de arquivos por extensão:" &&
find . -type f | awk -F. 'NF>1 {counts[$NF]++} END {for (ext in counts) print ext, counts[ext]}' | sort
echo "-> Tamanho total do diretório:" &&
du -s --block-size=1 | numfmt --to=iec --suffix=B
