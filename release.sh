#!/usr/bin/bash

gh release create $(cat VERSAO) IUNA.-.Modpack.zip -F MUDANCAS.md --title $(cat VERSAO) $@
