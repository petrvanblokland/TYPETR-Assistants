# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................
#
#   jills.py
#

JILLS_KERNING = (
    # Lowercase.
    'aaeaoaiauacadahamanarasatabagafalapavawayajakaqaxazaeeoeieuecedehemeneresetebegefelepeveweyejekeqeexezeooiouocodohomonorosotobogofol'+\
    'opovowoyojokoqoxozoiiuicidihiminirisitibigifilipiviwiyijikiqixiziuucuduhumunurusutubugufulupuvuwuyujukuquxuzuccdchcmcncrcsctcbcgcfcl'+\
    'cpcvcwcycjckcqcxczcddhdmdndrdsdtdbdgdfdldpdvdwdydjdkdqdxdzdhhmhnhrhshthbhghfhlhphvhwhyhjhkhqhxhzhmmmnmrmsmtmbmgmfmlmpmvmwmymjmkmqmxm'+\
    'zmnnrnsntnbngnfnlnpnvnwnynjnknqnxnznrrsrtrbrgrfrlrprvrwryrjrkrqrxrzrsstsbsgsfslspsvswsysjsksqsxszsttbtgtftltptvtwtytjtktqtxtztbbgbfb'+\
    'lbpbvbwbybjbkbqbxbzbggfglgpgvgwgygjgkgqgxgzgfflfpfvfwfyfjfkfqfxfzfllplvlwlyljlkllqlxlzlppvpwpypjpkpqppxpzpvvwvyvjvkvqvxvzvyywyyyjyky'+\
    'qyxyzyjjkjqjxjzjkkkqkxkzkqqxqzqxxzxzzaaeaoaiauacadahamanaraasatabagafalapavawayajakaqaxaeazaeeoeieuecedehemeneresetebegefelepeveweye'+\
    'jekeqeexezeooiouocodohomonoroosotobogofolopovowoyojokoqooxozoiiuicidihiminirisiitibigifilipiviwiyijikiqixiziuucuduhumunurusutuubuguf'+\
    'ulupuvuwuyujukuquxuzucccdchcmcncrcsctcbcgcfclccpcvcwcycjckcqcxczcddhdmdnddrdsdtdbdgdfdldpdvdwdydjddkdqdxdzdhhmhnhrhshthbhgfhlhphvhwh'+\
    'yhjhkhqhxhzhmmnmrmsmtmbmgmfmlmpmvmwmymmjmkmqmxmzmnnrnsntnbngnfnlnpnvnwnynjnknqnxnznrrsrrtrbrgrfrlrprvrwryrjrkrrqrxrzrsstsbsgsfslspsv'+\
    'swsyssjsksqsxszsttbtgtftltptvtwttytjtktqtxtztbbgbfblbpbbvbwbybjbkbqbxbzbggfglgpggvgwgygjgkgqgxgzgfflfpfvffwfyfjfkfqfxfzfllplvlwlyljl'+\
    'lklqlxlzlppvpwpypjpkpqppxpzpvvwvyvjvkvqvxvzvyywyyyjykyqyxyzyjjkjqjxjzjkkkqkkxkzkqqxqzqxxzxzz'+\
    '/h/e/space/i/s/space/b/u/t/space/a/n/space/i/t/space/a/t/space/t/h/e/space/s/h/e/space/d/o/space/o/n/space/h/i/s/space/n/o/t/space/l/i/k/e/space/o/f/space/t/h/e/m/space/a/r/e/space/a/s/space/t/h/e/y/space'+\
    '/c/a/n/space/b/o/t/h/space/b/e/space/f/o/r/space/o/r/space/b/e/space/i/n/space/w/i/t/h/space/h/i/s/space/t/o/o/space/i/n/space/f/r/o/m/space/w/e/r/e/space/b/y/space/o/n/l/y/space/s/o/m/e/space/h/e/r/space'+\
    '/h/a/v/e/space/t/o/space/a/f/t/e/r/space/t/h/a/t/space/t/h/a/n/space/w/h/i/c/h/space/y/o/u/space/a/l/s/o/space/h/a/d/space/e/i/t/h/e/r/space',

    # Capitals,
    'TaTbTcTdTeTfTgThTiTjTkTlTmTnToTpTqTrTsTtTuTvTwTxTyTzTœTæTßTfiTflVaVbVcVdVeVfVgVhViVjVkVlVmVnVoVpVqVrVsVtVuVvVwVxVyVzVœVæVßVfiVflWaWb'+\
    'WcWdWeWfWgWhWiWjWkWlWmWnWoWpWqWrWsWtWuWvWwWxWyWzWœWæWßWfiWflYaYbYcYdYeYfYgYhYiYjYkYlYmYnYoYpYqYrYsYtYuYvYwYxYyYzYœYæYßYfiYflKaKbKcKd'+\
    'KeKfKgKhKiKjKkKlKmKnKoKpKqKrKsKtKuKvKwKxKyKzRaRbRcRdReRfRgRhRiRjRkRlRmRnRoRpRqRrRsRtRuRvRwRxRyRzJaJbJcJdJeJfJgJhJiJjJkJlJmJnJoJpJqJr'+\
    'JsJtJuJvJwJxJyJzPaPbPcPdPePfPgPhPiPjPkPlPmPnPoPpPqPrPsPtPuPvPwPxPyPzFaFbFcFdFeFfFgFhFiFjFkFlFmFnFoFpFqFrFsFtFuFvFwFxFyFzAaAbAcAdAeAf'+\
    'AgAhAiAjAkAlAmAnAoApAqArAsAtAuAvAwAxAyAzAœAæAßAfiAflFœFæFßFfiFflKœKæKßKfiKflPœPæPßPfiPflLaLbLcLdLeLfLgLhLiLjLkLlLmLnLoLpLqLrLsLtLuLv'+\
    'LwLxLyLzLœLæLßLfiLflBaBbBcBdBeBfBgBhBiBjBkBlBmBnBoBpBqBrBsBtBuBvBwBxByBzBœBæBßBfiBflRœRæRßRfiRflSaSbScSdSeSfSgShSiSjSkSlSmSnSoSpSqSr'+\
    'SsStSuSvSwSxSySzSœSæSßSfiSflCaCbCcCdCeCfCgChCiCjCkClCmCnCoCpCqCrCsCtCuCvCwCxCyCzCœCæCßCfiCflDaDbDcDdDeDfDgDhDiDjDkDlDmDnDoDpDqDrDsDt'+\
    'DuDvDwDxDyDzDœDæDßDfiDflEaEbEcEdEeEfEgEhEiEjEkElEmEnEoEpEqErEsEtEuEvEwExEyEzEœEæEßEfiEflNaNbNcNdNeNfNgNhNiNjNkNlNmNnNoNpNqNrNsNtNuNv'+\
    'NwNxNyNzNœNæNßNfiNflGaGbGcGdGeGfGgGhGiGjGkGlGmGnGoGpGqGrGsGtGuGvGwGxGyGzGœGæGßGfiGflOaObOcOdOeOfOgOhOiOjOkOlOmOnOoOpOqOrOsOtOuOvOwOx'+\
    'OyOzOœOæOßOfiOflQaQbQcQdQeQfQgQhQiQjQkQlQmQnQoQpQqQrQsQtQuQvQwQxQyQzQœQæQßQfiQflHaHbHcHdHeHfHgHhHiHjHkHlHmHnHoHpHqHrHsHtHuHvHwHxHyHz'+\
    'HœHæHßHfiHflIaIbIcIdIeIfIgIhIiIjIkIlImInIoIpIqIrIsItIuIvIwIxIyIzIœIæIßIfiIflJœJæJßJfiJflMaMbMcMdMeMfMgMhMiMjMkMlMmMnMoMpMqMrMsMtMuMv'+\
    'MwMxMyMzMœMæMßMfiMflUaUbUcUdUeUfUgUhUiUjUkUlUmUnUoUpUqUrUsUtUuUvUwUxUyUzUœUæUßUfiUflXaXbXcXdXeXfXgXhXiXjXkXlXmXnXoXpXqXrXsXtXuXvXwXx'+\
    'XyXzXœXæXßXfiXflZaZbZcZdZeZfZgZhZiZjZkZlZmZnZoZpZqZrZsZtZuZvZwZxZyZzZœZæZßZfiZfl'+\
    'The His She Her It Some Only It’s Also That There Is He She They Any Who Which You What Where To On As At We If Any This In One Are '+\
    'After All How When Many My Do You Their ',

    'AAEAOAIAUACADAHAMANARASATABAGAFALAPAVAWAYAJAKAQAXAZAEEOEIEUECEDEHEMENERESETEBEGEFELEPEVEWEYEJEKEQEEXEZEOOIOUOCODOHOMONOROSOTOBOGOFOL'+\
    'OPOVOWOYOJOKOQOXOZOIIUICIDIHIMINIRISITIBIGIFILIPIVIWIYIJIKIQIXIZIUUCUDUHUMUNURUSUTUBUGUFULUPUVUWUYUJUKUQUXUZUCCDCHCMCNCRCSCTCBCGCFCL'+\
    'CPCVCWCYCJCKCQCXCZCDDHDMDNDRDSDTDBDGDFDLDPDVDWDYDJDKDQDXDZDHHMHNHRHSHTHBHGHFHLHPHVHWHYHJHKHQHXHZHMMMNMRMSMTMBMGMFMLMPMVMWMYMJMKMQMXM'+\
    'ZMNNRNSNTNBNGNFNLNPNVNWNYNJNKNQNXNZNRRSRTRBRGRFRLRPRVRWRYRJRKRQRXRZRSSTSBSGSFSLSPSVSWSYSJSKSQSXSZSTTBTGTFTLTPTVTWTYTJTKTQTXTZTBBGBFB'+\
    'LBPBVBWBYBJBKBQBXBZBGGFGLGPGVGWGYGJGKGQGXGZGFFLFPFVFWFYFJFKFQFXFZFLLPLVLWLYLJLKLLQLXLZLPPVPWPYPJPKPQPPXPZPVVWVYVJVKVQVXVZVYYWYYYJYKY'+\
    'QYXYZYJJKJQJXJZJKKKQKXKZKQQXQZQXXZXZZAAEAOAIAUACADAHAMANARAASATABAGAFALAPAVAWAYAJAKAQAXAEAZAEEOEIEUECEDEHEMENERESETEBEGEFELEPEVEWEYE'+\
    'JEKEQEEXEZEOOIOUOCODOHOMONOROOSOTOBOGOFOLOPOVOWOYOJOKOQOOXOZOIIUICIDIHIMINIRISIITIBIGIFILIPIVIWIYIJIKIQIXIZIUUCUDUHUMUNURUSUTUUBUGUF'+\
    'ULUPUVUWUYUJUKUQUXUZUCCCDCHCMCNCRCSCTCBCGCFCLCCPCVCWCYCJCKCQCXCZCDDHDMDNDDRDSDTDBDGDFDLDPDVDWDYDJDDKDQDXDZDHHMHNHRHSHTHBHGFHLHPHVHWH'+\
    'YHJHKHQHXHZHMMNMRMSMTMBMGMFMLMPMVMWMYMMJMKMQMXMZMNNRNSNTNBNGNFNLNPNVNWNYNJNKNQNXNZNRRSRRTRBRGRFRLRPRVRWRYRJRKRRQRXRZRSSTSBSGSFSLSPSV'+\
    'SWSYSSJSKSQSXSZSTTBTGTFTLTPTVTWTTYTJTKTQTXTZTBBGBFBLBPBBVBWBYBJBKBQBXBZBGGFGLGPGGVGWGYGJGKGQGXGZGFFLFPFVFFWFYFJFKFQFXFZFLLPLVLWLYLJL'+\
    'LKLQLXLZLPPVPWPYPJPKPQPPXPZPVVWVYVJVKVQVXVZVYYWYYYJYKYQYXYZYJJKJQJXJZJKKKQKKXKZKQQXQZQXXZXZZ'+\
    'HE IS BUT AN IT AT THE SHE DO ON HIS NOT LIKE OF THEM ARE AS THEY CAN BOTH BE FOR OR BE IN WITH HIS TOO IN FROM WERE BY ONLY SOME HER '+\
    'HAVE TO AFTER THAT THAN WHICH YOU ALSO HAD EITHER.',

    # Smallcaps.
    '/T/A.sc/T/B.sc/T/C.sc/T/D.sc/T/E.sc/T/F.sc/T/G.sc/T/H.sc/T/I.sc/T/J.sc/T/K.sc/T/L.sc/T/M.sc/T/N.sc/T/O.sc/T/P.sc/T/Q.sc/T/R.sc/T/S.sc'+\
    '/T/T.sc/T/U.sc/T/V.sc/T/W.sc/T/X.sc/T/Y.sc/T/Z.sc/T/OE.sc/T/AE.sc/T/ß/T/F.sc/I.sc/T/F.sc/L.sc/V/A.sc/V/B.sc/V/C.sc/V/D.sc/V/E.sc/V/F.sc'+\
    '/V/G.sc/V/H.sc/V/I.sc/V/J.sc/V/K.sc/V/L.sc/V/M.sc/V/N.sc/V/O.sc/V/P.sc/V/Q.sc/V/R.sc/V/S.sc/V/T.sc/V/U.sc/V/V.sc/V/W.sc/V/X.sc/V/Y.sc'+\
    '/V/Z.sc/V/OE.sc/V/AE.sc/V/ß/V/F.sc/I.sc/V/F.sc/L.sc/W/A.sc/W/B.sc/W/C.sc/W/D.sc/W/E.sc/W/F.sc/W/G.sc/W/H.sc/W/I.sc/W'+\
    '/J.sc/W/K.sc/W/L.sc/W/M.sc/W/N.sc/W/O.sc/W/P.sc/W/Q.sc/W/R.sc/W/S.sc/W/T.sc/W/U.sc/W/V.sc/W/W.sc/W/X.sc/W/Y.sc/W/Z.sc/W/OE.sc/W/AE.sc'+\
    '/W/ß/W/F.sc/I.sc/W/F.sc/L.sc/Y/A.sc/Y/B.sc/Y/C.sc/Y/D.sc/Y/E.sc/Y/F.sc/Y/G.sc/Y/H.sc/Y/I.sc/Y/J.sc/Y/K.sc/Y/L.sc/Y/M.sc/Y/N.sc/Y/O.sc'+\
    '/Y/P.sc/Y/Q.sc/Y/R.sc/Y/S.sc/Y/T.sc/Y/U.sc/Y/V.sc/Y/W.sc/Y/X.sc/Y/Y.sc/Y/Z.sc/Y/OE.sc/Y/AE.sc/Y/ß/Y/F.sc/I.sc/Y/F.sc/L.sc/K/A.sc/K/B.sc'+\
    '/K/C.sc/K/D.sc/K/E.sc/K/F.sc/K/G.sc/K/H.sc/K/I.sc/K/J.sc/K/K.sc/K/L.sc/K/M.sc/K/N.sc/K/O.sc/K/P.sc/K/Q.sc/K/R.sc/K/S.sc/K/T.sc'+\
    '/K/U.sc/K/V.sc/K/W.sc/K/X.sc/K/Y.sc/K/Z.sc/R/A.sc/R/B.sc/R/C.sc/R/D.sc/R/E.sc/R/F.sc/R/G.sc/R/H.sc/R/I.sc/R/J.sc/R/K.sc/R/L.sc/R/M.sc'+\
    '/R/N.sc/R/O.sc/R/P.sc/R/Q.sc/R/R.sc/R/S.sc/R/T.sc/R/U.sc/R/V.sc/R/W.sc/R/X.sc/R/Y.sc/R/Z.sc/J/A.sc/J/B.sc/J/C.sc/J/D.sc/J/E.sc/J/F.sc'+\
    '/J/G.sc/J/H.sc/J/I.sc/J/J.sc/J/K.sc/J/L.sc/J/M.sc/J/N.sc/J/O.sc/J/P.sc/J/Q.sc/J/R.sc/J/S.sc/J/T.sc/J/U.sc/J/V.sc/J/W.sc/J/X.sc/J/Y.sc'+\
    '/J/Z.sc/P/A.sc/P/B.sc/P/C.sc/P/D.sc/P/E.sc/P/F.sc/P/G.sc/P/H.sc/P/I.sc/P/J.sc/P/K.sc/P/L.sc/P/M.sc/P/N.sc/P/O.sc/P/P.sc/P/Q.sc/P/R.sc'+\
    '/P/S.sc/P/T.sc/P/U.sc/P/V.sc/P/W.sc/P/X.sc/P/Y.sc/P/Z.sc/F/A.sc/F/B.sc/F/C.sc/F/D.sc/F/E.sc/F/F.sc/F/G.sc/F/H.sc/F/I.sc/F/J.sc/F/K.sc'+\
    '/F/L.sc/F/M.sc/F/N.sc/F/O.sc/F/P.sc/F/Q.sc/F/R.sc/F/S.sc/F/T.sc/F/U.sc/F/V.sc/F/W.sc/F/X.sc/F/Y.sc/F/Z.sc/A/A.sc/A/B.sc/A/C.sc/A/D.sc'+\
    '/A/E.sc/A/F.sc/A/G.sc/A/H.sc/A/I.sc/A/J.sc/A/K.sc/A/L.sc/A/M.sc/A/N.sc/A/O.sc/A/P.sc/A/Q.sc/A/R.sc/A/S.sc/A/T.sc/A/U.sc/A/V.sc/A/W.sc'+\
    '/A/X.sc/A/Y.sc/A/Z.sc/A/OE.sc/A/AE.sc/A/ß/A/F.sc/I.sc/A/F.sc/L.sc/F/OE.sc/F/AE.sc/F/ß/F/F.sc/I.sc/F/F.sc/L.sc/K/OE.sc/K/AE.sc/K/ß/K'+\
    '/F.sc/I.sc/K/F.sc/L.sc/P/OE.sc/P/AE.sc/P/ß/P/F.sc/I.sc/P/F.sc/L.sc/L/A.sc/L/B.sc/L/C.sc/L/D.sc/L/E.sc/L/F.sc/L/G.sc/L/H.sc/L/I.sc/L'+\
    '/J.sc/L/K.sc/L/L.sc/L/M.sc/L/N.sc/L/O.sc/L/P.sc/L/Q.sc/L/R.sc/L/S.sc/L/T.sc/L/U.sc/L/V.sc/L/W.sc/L/X.sc/L/Y.sc/L/Z.sc/L/OE.sc/L/AE.sc'+\
    '/L/ß/L/F.sc/I.sc/L/F.sc/L.sc/B/A.sc/B/B.sc/B/C.sc/B/D.sc/B/E.sc/B/F.sc/B/G.sc/B/H.sc/B/I.sc/B/J.sc/B/K.sc/B/L.sc/B/M.sc/B/N.sc/B/O.sc'+\
    '/B/P.sc/B/Q.sc/B/R.sc/B/S.sc/B/T.sc/B/U.sc/B/V.sc/B/W.sc/B/X.sc/B/Y.sc/B/Z.sc/B/OE.sc/B/AE.sc/B/ß/B/F.sc/I.sc/B/F.sc/L.sc/R/OE.sc'+\
    '/R/AE.sc/R/ß/R/F.sc/I.sc/R/F.sc/L.sc/S/A.sc/S/B.sc/S/C.sc/S/D.sc/S/E.sc/S/F.sc/S/G.sc/S/H.sc/S/I.sc/S/J.sc/S/K.sc/S/L.sc/S/M.sc/S/N.sc'+\
    '/S/O.sc/S/P.sc/S/Q.sc/S/R.sc/S/S.sc/S/T.sc/S/U.sc/S/V.sc/S/W.sc/S/X.sc/S/Y.sc/S/Z.sc/S/OE.sc/S/AE.sc/S/ß/S/F.sc/I.sc/S/F.sc/L.sc/C/A.sc'+\
    '/C/B.sc/C/C.sc/C/D.sc/C/E.sc/C/F.sc/C/G.sc/C/H.sc/C/I.sc/C/J.sc/C/K.sc/C/L.sc/C/M.sc/C/N.sc/C/O.sc/C/P.sc/C/Q.sc/C/R.sc/C/S.sc/C/T.sc'+\
    '/C/U.sc/C/V.sc/C/W.sc/C/X.sc/C/Y.sc/C/Z.sc/C/OE.sc/C/AE.sc/C/ß/C/F.sc/I.sc/C/F.sc/L.sc/D/A.sc/D/B.sc/D/C.sc/D/D.sc/D/E.sc/D/F.sc/D/G.sc'+\
    '/D/H.sc/D/I.sc/D/J.sc/D/K.sc/D/L.sc/D/M.sc/D/N.sc/D/O.sc/D/P.sc/D/Q.sc/D/R.sc/D/S.sc/D/T.sc/D/U.sc/D/V.sc/D/W.sc/D/X.sc/D/Y.sc/D/Z.sc'+\
    '/D/OE.sc/D/AE.sc/D/ß/D/F.sc/I.sc/D/F.sc/L.sc/E/A.sc/E/B.sc/E/C.sc/E/D.sc/E/E.sc/E/F.sc/E/G.sc/E/H.sc/E/I.sc/E/J.sc/E/K.sc/E/L.sc/E/M.sc'+\
    '/E/N.sc/E/O.sc/E/P.sc/E/Q.sc/E/R.sc/E/S.sc/E/T.sc/E/U.sc/E/V.sc/E/W.sc/E/X.sc/E/Y.sc/E/Z.sc/E/OE.sc/E/AE.sc/E/ß/E/F.sc/I.sc/E/F.sc/L.sc'+\
    '/N/A.sc/N/B.sc/N/C.sc/N/D.sc/N/E.sc/N/F.sc/N/G.sc/N/H.sc/N/I.sc/N/J.sc/N/K.sc/N/L.sc/N/M.sc/N/N.sc/N/O.sc/N/P.sc/N/Q.sc/N/R.sc/N/S.sc'+\
    '/N/T.sc/N/U.sc/N/V.sc/N/W.sc/N/X.sc/N/Y.sc/N/Z.sc/N/OE.sc/N/AE.sc/N/ß/N/F.sc/I.sc/N/F.sc/L.sc/G/A.sc/G/B.sc/G/C.sc/G/D.sc/G/E.sc/G/F.sc'+\
    '/G/G.sc/G/H.sc/G/I.sc/G/J.sc/G/K.sc/G/L.sc/G/M.sc/G/N.sc/G/O.sc/G/P.sc/G/Q.sc/G/R.sc/G/S.sc/G/T.sc/G/U.sc/G/V.sc/G/W.sc/G/X.sc/G/Y.sc'+\
    '/G/Z.sc/G/OE.sc/G/AE.sc/G/ß/G/F.sc/I.sc/G/F.sc/L.sc/O/A.sc/O/B.sc/O/C.sc/O/D.sc/O/E.sc/O/F.sc/O/G.sc/O/H.sc/O/I.sc/O/J.sc/O/K.sc/O/L.sc'+\
    '/O/M.sc/O/N.sc/O/O.sc/O/P.sc/O/Q.sc/O/R.sc/O/S.sc/O/T.sc/O/U.sc/O/V.sc/O/W.sc/O/X.sc/O/Y.sc/O/Z.sc/O/OE.sc/O/AE.sc/O/ß/O/F.sc/I.sc/O/F.sc'+\
    '/L.sc/Q/A.sc/Q/B.sc/Q/C.sc/Q/D.sc/Q/E.sc/Q/F.sc/Q/G.sc/Q/H.sc/Q/I.sc/Q/J.sc/Q/K.sc/Q/L.sc/Q/M.sc/Q/N.sc/Q/O.sc/Q/P.sc/Q/Q.sc/Q/R.sc/Q/S.sc'+\
    '/Q/T.sc/Q/U.sc/Q/V.sc/Q/W.sc/Q/X.sc/Q/Y.sc/Q/Z.sc/Q/OE.sc/Q/AE.sc/Q/ß/Q/F.sc/I.sc/Q/F.sc/L.sc/H/A.sc/H/B.sc/H/C.sc/H/D.sc/H/E.sc/H/F.sc'+\
    '/H/G.sc/H/H.sc/H/I.sc/H/J.sc/H/K.sc/H/L.sc/H/M.sc/H/N.sc/H/O.sc/H/P.sc/H/Q.sc/H/R.sc/H/S.sc/H/T.sc/H/U.sc/H/V.sc/H/W.sc/H/X.sc/H/Y.sc/H/Z.sc'+\
    '/H/OE.sc/H/AE.sc/H/ß/H/F.sc/I.sc/H/F.sc/L.sc/I/A.sc/I/B.sc/I/C.sc/I/D.sc/I/E.sc/I/F.sc/I/G.sc/I/H.sc/I/I.sc/I/J.sc/I/K.sc/I/L.sc/I/M.sc'+\
    '/I/N.sc/I/O.sc/I/P.sc/I/Q.sc/I/R.sc/I/S.sc/I/T.sc/I/U.sc/I/V.sc/I/W.sc/I/X.sc/I/Y.sc/I/Z.sc/I/OE.sc/I/AE.sc/I/ß/I/F.sc/I.sc/I/F.sc/L.sc'+\
    '/J/OE.sc/J/AE.sc/J/ß/J/F.sc/I.sc/J/F.sc/L.sc/M/A.sc/M/B.sc/M/C.sc/M/D.sc/M/E.sc/M/F.sc/M/G.sc/M/H.sc/M/I.sc/M/J.sc/M/K.sc/M/L.sc/M/M.sc'+\
    '/M/N.sc/M/O.sc/M/P.sc/M/Q.sc/M/R.sc/M/S.sc/M/T.sc/M/U.sc/M/V.sc/M/W.sc/M/X.sc/M/Y.sc/M/Z.sc/M/OE.sc/M/AE.sc/M/ß/M/F.sc/I.sc/M/F.sc/L.sc'+\
    '/U/A.sc/U/B.sc/U/C.sc/U/D.sc/U/E.sc/U/F.sc/U/G.sc/U/H.sc/U/I.sc/U/J.sc/U/K.sc/U/L.sc/U/M.sc/U/N.sc/U/O.sc/U/P.sc/U/Q.sc/U/R.sc/U/S.sc/U'+\
    '/T.sc/U/U.sc/U/V.sc/U/W.sc/U/X.sc/U/Y.sc/U/Z.sc/U/OE.sc/U/AE.sc/U/ß/U/F.sc/I.sc/U/F.sc/L.sc/X/A.sc/X/B.sc/X/C.sc/X/D.sc/X/E.sc/X/F.sc/X'+\
    '/G.sc/X/H.sc/X/I.sc/X/J.sc/X/K.sc/X/L.sc/X/M.sc/X/N.sc/X/O.sc/X/P.sc/X/Q.sc/X/R.sc/X/S.sc/X/T.sc/X/U.sc/X/V.sc/X/W.sc/X/X.sc/X/Y.sc/X/Z.sc'+\
    '/X/OE.sc/X/AE.sc/X/ß/X/F.sc/I.sc/X/F.sc/L.sc/Z/A.sc/Z/B.sc/Z/C.sc/Z/D.sc/Z/E.sc/Z/F.sc/Z/G.sc/Z/H.sc/Z/I.sc/Z/J.sc/Z/K.sc/Z/L.sc/Z/M.sc'+\
    '/Z/N.sc/Z/O.sc/Z/P.sc/Z/Q.sc/Z/R.sc/Z/S.sc/Z/T.sc/Z/U.sc/Z/V.sc/Z/W.sc/Z/X.sc/Z/Y.sc/Z/Z.sc/Z/OE.sc/Z/AE.sc/Z/ß/Z/F.sc/I.sc/Z/F.sc/L.sc'+\
    '/H.sc/E.sc/space/H/I.sc/S.sc/space/S/H.sc/E.sc/space/H/E.sc/R.sc/space/I/T.sc/space/S/O.sc/M.sc/E.sc/space/O/N.sc/L.sc/Y.sc/space/I/T.sc'+\
    '/’/S.sc/space/A/L.sc/S.sc/O.sc/space/T/H.sc/A.sc/T.sc/space/T/H.sc/E.sc/R.sc/E.sc/space/I/S.sc/space/H/E.sc/space/S/H.sc/E.sc/space'+\
    '/T/H.sc/E.sc/Y.sc/space/A/N.sc/Y.sc/space/W/H.sc/O.sc/space/W/H.sc/I.sc/C.sc/H.sc/space/Y/O.sc/U.sc/space/W/H.sc/A.sc/T.sc/space/W/H.sc/E.sc'+\
    '/R.sc/E.sc/space/T/O.sc/space/O/N.sc/space/A/S.sc/space/A/T.sc/space/W/E.sc/space/I/F.sc/A/N.sc/Y.sc/space/T/H.sc/I.sc/S.sc/space/I'+\
    '/N.sc/space/O/N.sc/E.sc/space/A/R.sc/E.sc/space/A/F.sc/T.sc/E.sc/R.sc/space/A/L.sc/L.sc/space/H/O.sc/W.sc/space/W/H.sc/E.sc/N.sc'+\
    '/space/M/A.sc/N.sc/Y.sc/space/M/Y.sc/space/D/O.sc/space/Y/O.sc/U.sc/space/T/H.sc/E.sc/I.sc/R.sc',

    '/A.sc/A.sc/E.sc/A.sc/O.sc/A.sc/I.sc/A.sc/U.sc/A.sc/C.sc/A.sc/D.sc/A.sc/H.sc/A.sc/I.sc/A.sc/J.sc/A.sc/M.sc/A.sc/N.sc/A.sc/R.sc/A.sc/S.sc/A.sc/T.sc/A.sc/B.sc'+\
    '/A.sc/G.sc/A.sc/F.sc/A.sc/L.sc/A.sc/P.sc/A.sc/V.sc/A.sc/W.sc/A.sc/Y.sc/A.sc/J.sc/A.sc/K.sc/A.sc/Q.sc/A.sc/X.sc/A.sc/Z.sc/A.sc/E.sc/E.sc'+\
    '/O.sc/E.sc/I.sc/E.sc/U.sc/E.sc/C.sc/E.sc/D.sc/E.sc/H.sc/E.sc/I.sc/E.sc/J.sc/E.sc/M.sc/E.sc/N.sc/E.sc/R.sc/E.sc/S.sc/E.sc/T.sc/E.sc/B.sc/E.sc/G.sc/E.sc/F.sc'+\
    '/E.sc/L.sc/E.sc/P.sc/E.sc/V.sc/E.sc/W.sc/E.sc/Y.sc/E.sc/J.sc/E.sc/K.sc/E.sc/Q.sc/E.sc/E.sc/X.sc/E.sc/Z.sc/E.sc/O.sc/O.sc/I.sc/O.sc/U.sc'+\
    '/O.sc/C.sc/O.sc/D.sc/O.sc/H.sc/O.sc/I.sc/O.sc/J.sc/O.sc/M.sc/O.sc/N.sc/O.sc/R.sc/O.sc/S.sc/O.sc/T.sc/O.sc/B.sc/O.sc/G.sc/O.sc/F.sc/O.sc/L.sc'+\
    '/O.sc/P.sc/O.sc/V.sc/O.sc/W.sc/O.sc/Y.sc/O.sc/J.sc/O.sc/K.sc/O.sc/Q.sc/O.sc/X.sc/O.sc/Z.sc/O.sc/I.sc/I.sc/U.sc/I.sc/C.sc/I.sc/D.sc/I.sc'+\
    '/H.sc/I.sc/I.sc/I.sc/J.sc/I.sc/M.sc/I.sc/N.sc/I.sc/R.sc/I.sc/S.sc/I.sc/T.sc/I.sc/B.sc/I.sc/G.sc/I.sc/F.sc/I.sc/L.sc/I.sc/P.sc/I.sc/V.sc/I.sc/W.sc/I.sc/Y.sc'+\
    '/I.sc/J.sc/I.sc/K.sc/I.sc/Q.sc/I.sc/X.sc/I.sc/Z.sc/I.sc/U.sc/U.sc/C.sc/U.sc/D.sc/U.sc/H.sc/U.sc/I.sc/U.sc/J.sc/U.sc/M.sc/U.sc/N.sc/U.sc/R.sc/U.sc/S.sc/U.sc'+\
    '/T.sc/U.sc/B.sc/U.sc/G.sc/U.sc/F.sc/U.sc/L.sc/U.sc/P.sc/U.sc/V.sc/U.sc/W.sc/U.sc/Y.sc/U.sc/J.sc/U.sc/K.sc/U.sc/Q.sc/U.sc/X.sc/U.sc/Z.sc'+\
    '/U.sc/C.sc/C.sc/D.sc/C.sc/H.sc/C.sc/I.sc/C.sc/J.sc/C.sc/M.sc/C.sc/N.sc/C.sc/R.sc/C.sc/S.sc/C.sc/T.sc/C.sc/B.sc/C.sc/G.sc/C.sc/F.sc/C.sc/L.sc'+\
    '/C.sc/P.sc/C.sc/V.sc/C.sc/W.sc/C.sc/Y.sc/C.sc/J.sc/C.sc/K.sc/C.sc/Q.sc/C.sc/X.sc/C.sc/Z.sc/C.sc/D.sc/D.sc/H.sc/D.sc/I.sc/D.sc/J.sc/D.sc/M.sc/D.sc/N.sc/D.sc'+\
    '/R.sc/D.sc/S.sc/D.sc/T.sc/D.sc/B.sc/D.sc/G.sc/D.sc/F.sc/D.sc/L.sc/D.sc/P.sc/D.sc/V.sc/D.sc/W.sc/D.sc/Y.sc/D.sc/J.sc/D.sc/K.sc/D.sc/Q.sc'+\
    '/D.sc/X.sc/D.sc/Z.sc/D.sc/H.sc/D.sc/I.sc/D.sc/J.sc/H.sc/M.sc/H.sc/N.sc/H.sc/R.sc/H.sc/S.sc/H.sc/T.sc/H.sc/B.sc/H.sc/G.sc/H.sc/F.sc/H.sc/L.sc/H.sc/P.sc/H.sc'+\
    '/V.sc/H.sc/W.sc/H.sc/Y.sc/H.sc/I.sc/H.sc/J.sc/H.sc/K.sc/H.sc/Q.sc/H.sc/X.sc/H.sc/Z.sc/H.sc/M.sc/M.sc/M.sc/N.sc/M.sc/R.sc/M.sc/S.sc/M.sc/T.sc/M.sc'+\
    '/B.sc/M.sc/G.sc/M.sc/F.sc/M.sc/L.sc/M.sc/P.sc/M.sc/V.sc/M.sc/W.sc/M.sc/Y.sc/M.sc/J.sc/M.sc/K.sc/M.sc/Q.sc/M.sc/X.sc/M.sc'+\
    '/Z.sc/M.sc/N.sc/N.sc/R.sc/N.sc/S.sc/N.sc/T.sc/N.sc/B.sc/N.sc/G.sc/N.sc/F.sc/N.sc/L.sc/N.sc/P.sc/N.sc/V.sc/N.sc/W.sc/N.sc/Y.sc/N.sc/J.sc'+\
    '/N.sc/K.sc/N.sc/Q.sc/N.sc/X.sc/N.sc/Z.sc/N.sc/R.sc/R.sc/S.sc/R.sc/T.sc/R.sc/B.sc/R.sc/G.sc/R.sc/F.sc/R.sc/L.sc/R.sc/P.sc/R.sc/V.sc/R.sc'+\
    '/W.sc/R.sc/Y.sc/R.sc/J.sc/R.sc/K.sc/R.sc/Q.sc/R.sc/X.sc/R.sc/Z.sc/R.sc/S.sc/S.sc/T.sc/S.sc/B.sc/S.sc/G.sc/S.sc/F.sc/S.sc/L.sc/S.sc/P.sc'+\
    '/S.sc/V.sc/S.sc/W.sc/S.sc/Y.sc/S.sc/J.sc/S.sc/K.sc/S.sc/Q.sc/S.sc/X.sc/S.sc/Z.sc/S.sc/T.sc/T.sc/B.sc/T.sc/G.sc/T.sc/F.sc/T.sc/L.sc/T.sc'+\
    '/P.sc/T.sc/V.sc/T.sc/W.sc/T.sc/Y.sc/T.sc/J.sc/T.sc/K.sc/T.sc/Q.sc/T.sc/X.sc/T.sc/Z.sc/T.sc/B.sc/B.sc/G.sc/B.sc/F.sc/B.sc'+\
    '/L.sc/B.sc/P.sc/B.sc/V.sc/B.sc/W.sc/B.sc/Y.sc/B.sc/J.sc/B.sc/K.sc/B.sc/Q.sc/B.sc/X.sc/B.sc/Z.sc/B.sc/G.sc/G.sc/F.sc/G.sc/L.sc/G.sc/P.sc'+\
    '/G.sc/V.sc/G.sc/W.sc/G.sc/Y.sc/G.sc/J.sc/G.sc/K.sc/G.sc/Q.sc/G.sc/X.sc/G.sc/Z.sc/G.sc/F.sc/F.sc/L.sc/F.sc/P.sc/F.sc/V.sc/F.sc/W.sc/F.sc'+\
    '/Y.sc/F.sc/J.sc/F.sc/K.sc/F.sc/Q.sc/F.sc/X.sc/F.sc/Z.sc/F.sc/L.sc/L.sc/P.sc/L.sc/V.sc/L.sc/W.sc/L.sc/Y.sc/L.sc/J.sc/L.sc/K.sc/L.sc/L.sc'+\
    '/Q.sc/L.sc/X.sc/L.sc/Z.sc/L.sc/P.sc/P.sc/V.sc/P.sc/W.sc/P.sc/Y.sc/P.sc/J.sc/P.sc/K.sc/P.sc/Q.sc/P.sc/P.sc/X.sc/P.sc/Z.sc/P.sc/V.sc/V.sc'+\
    '/W.sc/V.sc/Y.sc/V.sc/J.sc/V.sc/K.sc/V.sc/Q.sc/V.sc/X.sc/V.sc/Z.sc/V.sc/Y.sc/Y.sc/W.sc/Y.sc/Y.sc/Y.sc/J.sc/Y.sc/K.sc/Y.sc'+\
    '/Q.sc/Y.sc/X.sc/Y.sc/Z.sc/Y.sc/J.sc/J.sc/K.sc/J.sc/Q.sc/J.sc/X.sc/J.sc/Z.sc/J.sc/K.sc/K.sc/K.sc/Q.sc/K.sc/X.sc/K.sc/Z.sc/K.sc/Q.sc/Q.sc'+\
    '/X.sc/Q.sc/Z.sc/Q.sc/X.sc/X.sc/Z.sc/X.sc/Z.sc/Z.sc/A.sc/A.sc/E.sc/A.sc/O.sc/A.sc/I.sc/A.sc/U.sc/A.sc/C.sc/A.sc/D.sc/A.sc/H.sc/A.sc/I.sc/A.sc/J.sc/A.sc/M.sc'+\
    '/A.sc/N.sc/A.sc/R.sc/A.sc/A.sc/S.sc/A.sc/T.sc/A.sc/B.sc/A.sc/G.sc/A.sc/F.sc/A.sc/L.sc/A.sc/P.sc/A.sc/V.sc/A.sc/W.sc/A.sc/Y.sc/A.sc/J.sc'+\
    '/A.sc/K.sc/A.sc/Q.sc/A.sc/X.sc/A.sc/E.sc/A.sc/Z.sc/A.sc/E.sc/E.sc/O.sc/E.sc/I.sc/E.sc/U.sc/E.sc/C.sc/E.sc/D.sc/E.sc/H.scE.sc/I.scE.sc/J.sc/E.sc/M.sc/E.sc'+\
    '/N.sc/E.sc/R.sc/E.sc/S.sc/E.sc/T.sc/E.sc/B.sc/E.sc/G.sc/E.sc/F.sc/E.sc/L.sc/E.sc/P.sc/E.sc/V.sc/E.sc/W.sc/E.sc/Y.sc/E.sc'+\
    '/J.sc/E.sc/K.sc/E.sc/Q.sc/E.sc/E.sc/X.sc/E.sc/Z.sc/E.sc/O.sc/O.sc/I.sc/O.sc/U.sc/O.sc/C.sc/O.sc/D.sc/O.sc/H.sc/O.sc/I.sc/O.sc/J.sc/O.sc/M.sc/O.sc/N.sc/O.sc'+\
    '/R.sc/O.sc/O.sc/S.sc/O.sc/T.sc/O.sc/B.sc/O.sc/G.sc/O.sc/F.sc/O.sc/L.sc/O.sc/P.sc/O.sc/V.sc/O.sc/W.sc/O.sc/Y.sc/O.sc/J.sc/O.sc/K.sc/O.sc'+\
    '/Q.sc/O.sc/O.sc/X.sc/O.sc/Z.sc/O.sc/I.sc/I.sc/U.sc/I.sc/C.sc/I.sc/D.sc/I.sc/H.sc/I.sc/J.sc/I.sc/M.sc/I.sc/N.sc/I.sc/R.sc/I.sc/S.sc/I.sc/I.sc/T.sc'+\
    '/I.sc/B.sc/I.sc/G.sc/I.sc/F.sc/I.sc/L.sc/I.sc/P.sc/I.sc/V.sc/I.sc/W.sc/I.sc/Y.sc/I.sc/J.sc/I.sc/K.sc/I.sc/Q.sc/I.sc/X.sc/I.sc/Z.sc/I.sc'+\
    '/U.sc/U.sc/C.sc/U.sc/D.sc/U.sc/H.sc/U.sc/I.sc/U.sc/J.sc/U.sc/M.sc/U.sc/N.sc/U.sc/R.sc/U.sc/S.sc/U.sc/T.sc/U.sc/U.sc/B.sc/U.sc/G.sc/U.sc/F.sc'+\
    '/U.sc/L.sc/U.sc/P.sc/U.sc/V.sc/U.sc/W.sc/U.sc/Y.sc/U.sc/J.sc/U.sc/K.sc/U.sc/Q.sc/U.sc/X.sc/U.sc/Z.sc/U.sc/C.sc/C.sc/C.sc/D.sc/C.sc/H.sc/C.sc/I.sc/C.sc/J.sc'+\
    '/C.sc/M.sc/C.sc/N.sc/C.sc/R.sc/C.sc/S.sc/C.sc/T.sc/C.sc/B.sc/C.sc/G.sc/C.sc/F.sc/C.sc/L.sc/C.sc/C.sc/P.sc/C.sc/V.sc/C.sc/W.sc/C.sc/Y.sc'+\
    '/C.sc/J.sc/C.sc/K.sc/C.sc/Q.sc/C.sc/X.sc/C.sc/Z.sc/C.sc/D.sc/D.sc/H.sc/D.sc/I.sc/D.sc/J.sc/D.sc/M.sc/D.sc/N.sc/D.sc/D.sc/R.sc/D.sc/S.sc/D.sc/T.sc/D.sc/B.sc'+\
    '/D.sc/G.sc/D.sc/F.sc/D.sc/L.sc/D.sc/P.sc/D.sc/V.sc/D.sc/W.sc/D.sc/Y.sc/D.sc/J.sc/D.sc/D.sc/K.sc/D.sc/Q.sc/D.sc/X.sc/D.sc/Z.sc/D.sc/H.sc/D.sc/I.sc/D.sc/J.sc'+\
    '/H.sc/M.sc/H.sc/N.sc/H.sc/R.sc/H.sc/S.sc/H.sc/T.sc/H.sc/B.sc/H.sc/G.sc/F.sc/H.sc/L.sc/H.sc/P.sc/H.sc/V.sc/H.sc/W.sc/H.sc'+\
    '/Y.sc/H.sc/J.sc/H.sc/K.sc/H.sc/Q.sc/H.sc/X.sc/H.sc/Z.sc/H.sc/M.sc/M.sc/N.sc/M.sc/R.sc/M.sc/S.sc/M.sc/T.sc/M.sc/B.sc/M.sc/G.sc/M.sc/F.sc'+\
    '/M.sc/L.sc/M.sc/P.sc/M.sc/V.sc/M.sc/W.sc/M.sc/Y.sc/M.sc/M.sc/J.sc/M.sc/K.sc/M.sc/Q.sc/M.sc/X.sc/M.sc/Z.sc/M.sc/N.sc/N.sc/R.sc/N.sc/S.sc'+\
    '/N.sc/T.sc/N.sc/B.sc/N.sc/G.sc/N.sc/F.sc/N.sc/L.sc/N.sc/P.sc/N.sc/V.sc/N.sc/W.sc/N.sc/Y.sc/N.sc/J.sc/N.sc/K.sc/N.sc/Q.sc/N.sc/X.sc/N.sc'+\
    '/Z.sc/N.sc/R.sc/R.sc/S.sc/R.sc/R.sc/T.sc/R.sc/B.sc/R.sc/G.sc/R.sc/F.sc/R.sc/L.sc/R.sc/P.sc/R.sc/V.sc/R.sc/W.sc/R.sc/Y.sc/R.sc/J.sc/R.sc'+\
    '/K.sc/R.sc/R.sc/Q.sc/R.sc/X.sc/R.sc/Z.sc/R.sc/S.sc/S.sc/T.sc/S.sc/B.sc/S.sc/G.sc/S.sc/F.sc/S.sc/L.sc/S.sc/P.sc/S.sc/V.sc'+\
    '/S.sc/W.sc/S.sc/Y.sc/S.sc/S.sc/J.sc/S.sc/K.sc/S.sc/Q.sc/S.sc/X.sc/S.sc/Z.sc/S.sc/T.sc/T.sc/B.sc/T.sc/G.sc/T.sc/F.sc/T.sc/L.sc/T.sc/P.sc'+\
    '/T.sc/V.sc/T.sc/W.sc/T.sc/T.sc/Y.sc/T.sc/J.sc/T.sc/K.sc/T.sc/Q.sc/T.sc/X.sc/T.sc/Z.sc/T.sc/B.sc/B.sc/G.sc/B.sc/F.sc/B.sc/L.sc/B.sc/P.sc'+\
    '/B.sc/B.sc/V.sc/B.sc/W.sc/B.sc/Y.sc/B.sc/J.sc/B.sc/K.sc/B.sc/Q.sc/B.sc/X.sc/B.sc/Z.sc/B.sc/G.sc/G.sc/F.sc/G.sc/L.sc/G.sc/P.sc/G.sc/G.sc'+\
    '/V.sc/G.sc/W.sc/G.sc/Y.sc/G.sc/J.sc/G.sc/K.sc/G.sc/Q.sc/G.sc/X.sc/G.sc/Z.sc/G.sc/F.sc/F.sc/L.sc/F.sc/P.sc/F.sc/V.sc/F.sc/F.sc/W.sc/F.sc'+\
    '/Y.sc/F.sc/J.sc/F.sc/K.sc/F.sc/Q.sc/F.sc/X.sc/F.sc/Z.sc/F.sc/L.sc/L.sc/P.sc/L.sc/V.sc/L.sc/W.sc/L.sc/Y.sc/L.sc/J.sc/L.sc'+\
    '/L.sc/K.sc/L.sc/Q.sc/L.sc/X.sc/L.sc/Z.sc/L.sc/P.sc/P.sc/V.sc/P.sc/W.sc/P.sc/Y.sc/P.sc/J.sc/P.sc/K.sc/P.sc/Q.sc/P.sc/P.sc/X.sc/P.sc/Z.sc'+\
    '/P.sc/V.sc/V.sc/W.sc/V.sc/Y.sc/V.sc/J.sc/V.sc/K.sc/V.sc/Q.sc/V.sc/X.sc/V.sc/Z.sc/V.sc/Y.sc/Y.sc/W.sc/Y.sc/Y.sc/Y.sc/J.sc/Y.sc/K.sc/Y.sc'+\
    '/Q.sc/Y.sc/X.sc/Y.sc/Z.sc/Y.sc/J.sc/J.sc/K.sc/J.sc/Q.sc/J.sc/X.sc/J.sc/Z.sc/J.sc/K.sc/K.sc/K.sc/Q.sc/K.sc/K.sc/X.sc/K.sc/Z.sc/K.sc/Q.sc'+\
    '/Q.sc/X.sc/Q.sc/Z.sc/Q.sc/X.sc/X.sc/Z.sc/X.sc/Z.sc/Z.sc'+\
    '/H.sc/E.sc/space/I.sc/S.sc/space/B.sc/U.sc/T.sc/space/A.sc/N.sc/space/I.sc/T.sc/space/A.sc/T.sc/space/T.sc/H.sc/E.sc/space/S.sc/H.sc/E.sc/space/D.sc/O.sc/space/O.sc/N.sc/space'+\
    '/H.sc/I.sc/S.sc/space/N.sc/O.sc/T.sc/space/L.sc/I.sc/K.sc/E.sc/space/O.sc/F.sc/space/T.sc/H.sc/E.sc/M.sc/space/A.sc/R.sc/E.sc/space/A.sc/S.sc/space/T.sc/H.sc/E.sc/Y.sc/space'+\
    '/C.sc/A.sc/N.sc/space/B.sc/O.sc/T.sc/H.sc/space/B.sc/E.sc/space/F.sc/O.sc/R.sc/space/O.sc/R.sc/space/B.sc/E.sc/space/I.sc/N.sc/space/W.sc/I.sc/T.sc/H.sc/space/H.sc/I.sc/S.sc/space'+\
    '/T.sc/O.sc/O.sc/space/I.sc/N.sc/space/F.sc/R.sc/O.sc/M.sc/space/W.sc/E.sc/R.sc/E.sc/space/B.sc/Y.sc/space/O.sc/N.sc/L.sc/Y.sc/space/S.sc/O.sc/M.sc/E.sc/space'+\
    '/H.sc/E.sc/R.sc/space/H.sc/A.sc/V.sc/E.sc/space/T.sc/O.sc/space/A.sc/F.sc/T.sc/E.sc/R.sc/space/T.sc/H.sc/A.sc/T.sc/space/T.sc/H.sc/A.sc/N.sc/space'+\
    '/W.sc/H.sc/I.sc/C.sc/H.sc/space/Y.sc/O.sc/U.sc/space/A.sc/L.sc/S.sc/O.sc/space/H.sc/A.sc/D.sc/space/E.sc/I.sc/T.sc/H.sc/E.sc/R.sc/period',

    '010203040506070809000.0,0;0:00<0>0=0+0$000£000¥000ƒ000#000§000¶000000%000‰000¢000ª000º112131415161718191011.1,1;1:1<1>1=1+1$100£100¥'+\
    '100ƒ100#100§100¶100001%001‰001¢001ª001º212232425262728292022.2,2;2:22<2>2=2+2$200£200¥200ƒ200#200§200¶200002%002‰002¢002ª002º3132334'+\
    '35363738393033.3,3;3:33<3>3=3+3$300£300¥300ƒ300#300§300¶300003%003‰003¢003ª003º414243445464748494044.4,4;4:44<4>4=4+4$400£400¥400ƒ40'+\
    '0#400§400¶400004%004‰004¢004ª004º515253545565758595055.5,5;5:55<5>5=5+5$500£500¥500ƒ500#500§500¶500005%005‰005¢005ª005º6162636465667'+\
    '68696066.6,6;6:66<6>6=6+6$600£600¥600ƒ600#600§600¶600006%006‰006¢006ª006º717273747576778797077.7,7;7:77<7>7=7+7$700£700¥700ƒ700#700§'+\
    '700¶700007%007‰007¢007ª007º818283848586878898088.8,8;8:88<8>8=8+8$800£800¥800ƒ800#800§800¶800008%008‰008¢008ª008º9192939495969798990'+\
    '99.9,9;9:9<9>9=9+9$900£900¥900ƒ900#900§900¶900009%009‰009¢009ª009º0/slash/one/slash/two/slash/three/slash/four/slash/five/slash/six/slash/seven/slash/eight/slash/nine/slash/zero/slash .a.b.c.d.e.f.g.h.i.j.k.'+\
    'l.m.n.o.p.q.r.s.t.u.v.w.x.y.z.,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,/slash/a/slash/b/slash/c/slash/d/slash/e/slash/f/slash/g/slash/h/slash/i/slash/j/slash/k/slash/l/slash/m/slash/n/slash/o/slash/p/slash/q/slash/r/slash/s/slash/t/slash/u/slash/v/slash/w/slash/x'+\
    '/slash/y/slash/z \\a\\b\\c\\d\\e\\f\\g\\h\\i\\j\\k\\l\\m\\n\\o\\p\\q\\r\\s\\t\\u\\v\\w\\x\\y\\z\\a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z:a;b;c;d;e;f;g;h;i;j;k;l'+\
    ';m;n;o;p;q;r;s;t;u;v;w;x;y;z;¡a!¡b!¡c!¡d!¡e!¡f!¡g!¡h!¡i!¡j!¡k!¡l!¡m!¡n!¡o!¡p!¡q!¡r!¡s!¡t!¡u!¡v!¡w!¡x!¡y!¡z!¿a?¿b?¿c?¿d?¿e?¿f?¿g?¿h?¿'+\
    'i?¿j?¿k?¿l?¿m?¿n?¿o?¿p?¿q?¿r?¿s?¿t?¿u?¿v?¿w?¿x?¿y?¿z?(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)(k)(l)(m)(n)(o)(p)(q)(r)(s)(t)(u)(v)(w)(x)(y)(z)['+\
    'a][b][c][d][e][f][g][h][i][j][k][l][m][n][o][p][q][r][s][t][u][v][w][x][y][z]{a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n}{o}{p}{q}{r}{'+\
    's}{t}{u}{v}{w}{x}{y}{z}“a”“b”“c”“d”“e”“f”“g”“h”“i”“j”“k”“l”“m”“n”“o”“p”“q”“r”“s”“t”“u”“v”“w”“x”“y”“z”‘a’‘b’‘c’‘d’‘e’‘f’‘g’‘h’‘i’‘j’‘'+\
    'k’‘l’‘m’‘n’‘o’‘p’‘q’‘r’‘s’‘t’‘u’‘v’‘w’‘x’‘y’‘z’’a’b’c’d’e’f’g’h’i’j’k’l’m’n’o’p’q’r’s’t’u’v’w’x’y’z’«a»«b»«c»«d»«e»«f»«g»«h»«i»«j»«k'+\
    '»«l»«m»«n»«o»«p»«q»«r»«s»«t»«u»«v»«w»«x»«y»«z»‹a›‹b›‹c›‹d›‹e›‹f›‹g›‹h›‹i›‹j›‹k›‹l›‹m›‹n›‹o›‹p›‹q›‹r›‹s›‹t›‹u›‹v›‹w›‹x›‹y›‹z›»a«»b«»c'+\
    '«»d«»e«»f«»g«»h«»i«»j«»k«»l«»m«»n«»o«»p«»q«»r«»s«»t«»u«»v«»w«»x«»y«»z«›a‹›b‹›c‹›d‹›e‹›f‹›g‹›h‹›i‹›j‹›k‹›l‹›m‹›n‹›o‹›p‹›q‹›r‹›s‹›t‹›u‹'+\
    '›v‹›w‹›x‹›y‹›z‹*a*b*c*d*e*f*g*h*i*j*k*l*m*n*o*p**q*r*s*t*u*v*w*x*y*z*®a®b®c®d®e®f®g®h®i®j®k®l®m®n®o®p®q®r®s®t®u®v®w®x®y®z®™a™b™c™d™e'+\
    '™f™g™h™i™j™k™l™m™n™o™p™q™r™s™t™u™v™w™x™y™z™&a@a@b@c@d@e@f@g@h@i@j@k@l@m@n@o@p@q@r@s@t@u@v@w@x@y@z@-a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q'+\
    '-r-s-t-u-v-w-x-y-z--a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z-æaæbæcædææeæfægæhæiæjækælæmænæoææpæqæræsætæuævæwæxæyæzæœaœbœ'+\
    'cœdœeœfœgœhœiœjœkœlœmœœnœoœpœqœrœsœtœuœvœwœxœyœzœßaßbßcßdßeßfßgßhßißjßkßßlßmßnßoßpßqßrßsßtßußvßwßxßyßzß .A.B.C.D.E.F.G.H.I.J.K.L.M.N'+\
    '.O.P.Q.R.S.T.U.V.W.X.Y.Z.,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,/slash/A/slash/B/slash/C/slash/D/slash/E/slash/F/slash/G/slash/H/slash/I/slash/J/slash/K/slash/L/slash/M/slash/N/slash/O/slash/P/slash/Q/slash/R/slash/S/slash/T/slash/U/slash/V/slash/W/slash/X/slash/Y/slash/Z/slash/\\A'+\
    '\\B\\C\\D\\E\\F\\G\\H\\I\\J\\K\\L\\M\\N\\O\\P\\Q\\R\\S\\T\\U\\V\\W\\X\\Y\\Z\\A:B:C:D:E:F:G:H:I:J:K:L:M:N:O:P:Q:R:S:T:U:V:W:X:Y:Z:A;B;C;D;E;F;G;H;I;J;K;L;M;N;O'+\
    ';P;Q;R;S;T;U;V;W;X;Y;Z;¡A!¡B!¡C!¡D!¡E!¡F!¡G!¡H!¡I!¡J!¡K!¡L!¡M!¡N!¡O!¡P!¡Q!¡R!¡S!¡T!¡U!¡V!¡W!¡X!¡Y!¡Z!¿A?¿B?¿C?¿D?¿E?¿F?¿G?¿H?¿I?¿J?'+\
    '¿K?¿L?¿M?¿N?¿O?¿P?¿Q?¿R?¿S?¿T?¿U?¿V?¿W?¿X?¿Y?¿Z?(A)(B)(C)(D)(E)(F)(G)(H)(I)(J)(K)(L)(M)(N)(O)(P)(Q)(R)(S)(T)(U)(V)(W)(X)(Y)(Z)[A][B'+\
    '][C][D][E][F][G][H][I][J][K][L][M][N][O][P][Q][R][S][T][U][V][W][X][Y][Z]{A}{B}{C}{D}{E}{F}{G}{H}{I}{J}{K}{L}{M}{N}{O}{P}{Q}{R}{S}{T'+\
    '}{U}{V}{W}{X}{Y}{Z}“A”“B”“C”“D”“E”“F”“G”“H”“I”“J”“K”“L”“M”“N”“O”“P”“Q”“R”“S”“T”“U”“V”“W”“X”“Y”“Z”‘A’‘B’‘C’‘D’‘E’‘F’‘G’‘H’‘I’‘J’‘K’‘L'+\
    '’‘M’‘N’‘O’‘P’‘Q’‘R’‘S’‘T’‘U’‘V’‘W’‘X’‘Y’‘Z’’A’B’C’D’E’F’G’H’I’J’K’L’M’N’O’P’Q’R’S’T’U’V’W’X’Y’Z’«A»«B»«C»«D»«E»«F»«G»«H»«I»«J»«K»«L»«'+\
    'M»«N»«O»«P»«Q»«R»«S»«T»«U»«V»«W»«X»«Y»«Z»‹A›‹B›‹C›‹D›‹E›‹F›‹G›‹H›‹I›‹J›‹K›‹L›‹M›‹N›‹O›‹P›‹Q›‹R›‹S›‹T›‹U›‹V›‹W›‹X›‹Y›‹Z›»A«»B«»C«»D«»E'+\
    '«»F«»G«»H«»I«»J«»K«»L«»M«»N«»O«»P«»Q«»R«»S«»T«»U«»V«»W«»X«»Y«»Z«›A‹›B‹›C‹›D‹›E‹›F‹›G‹›H‹›I‹›J‹›K‹›L‹›M‹›N‹›O‹›P‹›Q‹›R‹›S‹›T‹›U‹›V‹›W‹›'+\
    'X‹›Y‹›Z‹*A*B*C*D*E*F*G*H*I*J*K*L*M*N*O*P**Q*R*S*T*U*V*W*X*Y*Z*®A®B®C®D®E®F®G®H®I®J®K®L®M®N®O®P®Q®R®S®T®U®V®W®X®Y®Z®™A™B™C™D™E™F™G™H™I'+\
    '™J™K™L™M™N™O™P™Q™R™S™T™U™V™W™X™Y™Z™&A@A@B@C@D@E@F@G@H@I@J@K@L@M@N@O@P@Q@R@S@T@U@V@W@X@Y@Z@-A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-'+\
    'V-W-X-Y-Z--A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z-æAæBæCæDææEæFæGæHæIæJæKæLæMæNæOææPæQæRæSæTæUæVæWæXæYæZæœAœBœCœDœEœFœGœ'+\
    'HœIœJœKœLœMœœNœOœPœQœRœSœTœUœVœWœXœYœZœßAßBßCßDßEßFßGßHßIßJßKßßLßMßNßOßPßQßRßSßTßUßVßWßXßYßZß “¿Que?” “¡Que!” “nn.” “nn,” “nn”. “nn”,  Fin.'
)

JILLS_KERNING = ''.join(JILLS_KERNING)

EXTENDED_KERNING = (
    u'áán ààn åån ään ábn àbn ăbn âbn åbn äbn ābn áčn äčn āčn áðn áén áfn àfn ăfn âfn åfn äfn āfn âğn āģn áhn àhn åhn ähn áin '+\
        u'áín àin ăin âin åin äin āin ájn ăjn åjn äjn ājn ákn âkn åkn äkn ākn āķn áln áľn àln ăln âln åln äln āln āļn áňn áñn '+\
        u'áón äön ářn ášn āšn äßn átn áťn àtn ătn ățn âtn âțn åtn ätn äťn ātn ážn āžn áþn',
    u'čán čān ćbn čbn ččn ċċn čėn čēn ćfn čfn ċħn ćin čin čín čīn ċin ćjn čjn ċjn ćkn čkn ċkn ćln čln čľn ċln čňn čŕn čšn čtn '+\
        u'ċtn čún čůn čūn dán dàn dăn dân dån dän dãn dān ďan ďán ðán dčn dén dèn děn dën dēn dħn dìn dîn dīn đin ðín ďkn ďmn '+\
        u'dňn ďnn dòn dôn dön dőn dõn ďon ðón ðön dřn dšn ďsn ďtn dùn důn dün dūn ďun džn ďžn',
    u'éán éân éån ébn èbn ěbn ëbn ēbn éčn ěčn ėčn éðn ěďn één éèn éfn èfn ëfn ēfn ēģn éhn ěhn ëhn éin èin êin ëin ėin éjn èjn '+\
        u'ějn ëjn ėjn ējn ékn ěkn ëkn ēkn ēķn éln èln êln ěln ëln ēln ēļn ěňn éřn ěřn éšn ěšn ėšn ēšn étn ètn êtn ětn ěťn ëtn '+\
        u'ėtn ētn éün éžn ěžn ėžn ēžn fán fàn făn fân fån fän fãn fān fén fèn fên fën fėn fēn fħn fín fīn fňn fón fòn fön főn '+\
        u'fõn fšn fún fûn fůn fün fűn fūn',
    u'ġàn ģān ğbn ģēn ğfn ġġn ğin ġin ģīn ġjn ğln ğtn ġtn ğün ġżn',
    u'hán ħġn ħħn',
    u'ián iàn iân iån iän iãn iān íán íbn ïbn ībn ićn ičn iċn íčn īčn iđn íðn ién ièn iên iën iėn iēn íén įėn ífn ïfn īfn iğn '+\
        u'iġn īģn iħn íhn īhn iín iîn iïn ïïn iīn íin îin íjn ïjn ījn íkn îkn ïkn īkn īķn íln íľn îln ïln īln īļn iňn iñn íňn '+\
        u'íñn ión iòn iôn iön iőn iõn íón iřn ířn iśn išn íšn įšn īšn ítn íťn ìtn îtn îțn ïtn ītn iùn iůn iün iūn iźn ižn iżn '+\
        u'ížn įžn īžn íþn',
    u'ján jàn jăn jân jån jän jãn jān jčn jċn jén jèn jën jėn jēn jġn jħn jín jīn jňn jón jòn jôn jön jőn jõn jřn jśn jšn jún '+\
        u'jůn jün jūn jžn jżn lán làn lăn lân lån län lãn lān ľan ļān ľbn lčn ľčn ľdn lén lèn lên lën lēn ļēn lğn ľgn lħn ľhn '+\
        u'lìn lîn līn ļīn ľjn ľkn ļķn ľmn lńn lňn ĺňn ľnn ľňn lòn lôn lön lőn lõn ľon łón ľrn lšn ľsn ľšn ļšn ľtn łtn lùn lůn '+\
        u'lün lūn ľun ľún ļūn ľvn lžn ĺžn ľžn ļžn',
    u'ňán ñán ñén ňhn ñin ñín ńkn ňkn ñón ňůn',
    u'óán öän őán óbn ôbn öbn őbn õbn óčn ôčn óðn öðn óén őén ófn öfn őfn öğn óhn ôhn öhn őhn õhn óin óín öin őin őín õin ójn '+\
        u'ôjn öjn őjn õjn ókn ôkn ökn őkn õkn óln ółn ôln ôľn öln őln õln óňn ôňn óón óön öön öõn őón őön őőn õõn óśn ôšn ößn '+\
        u'ótn ôtn ôťn ötn őtn õtn óún óün őún őün óźn óžn óżn ôžn óþn',
    u'řán řbn ŕčn řčn ŕhn řin řín řkn řln ŕňn řňn ŕšn řšn ŕtn řtn řůn ŕžn',
    u'šán šān śbn šbn śćn šćn ščn šén šėn šēn šģn šhn šin šín šįn šīn šjn škn šķn śln šln šľn šļn śńn šňn ššn ßön štn šťn šún '+\
        u'šůn šün šūn šžn',
    u'tán tàn tăn tân tån tän tãn tān ťan ťán țăn țân tċn ťcn ťčn ťdn tén tèn tên těn tën tėn tēn tħn ťhn tìn tîn tīn ťjn ťkn '+\
        u'ťln ťmn tňn ťnn tón tòn tôn tön tőn tõn ťon ťpn tŕn třn ťrn tšn ťsn ťšn ťtn tùn tůn tün tūn ťun ťůn tžn',
    u'úán üän úbn ůbn übn űbn ūbn účn ůčn ūčn úðn üén üèn úfn üfn űfn ūfn üğn úhn ůhn ühn űhn ūhn úin úín üin üín űin újn ůjn '+\
        u'üjn űjn ūjn úkn ůkn ükn űkn ūkn ūķn úln úľn ûln ůln üln űln ūln ūļn úňn úñn úřn ůřn úšn ūšn üßn útn úťn ûtn ůtn ütn '+\
        u'űtn ūtn üün úžn ůžn ūžn',
    u'ýán ýbn ýčn ýðn ýfn ýhn ýin ýjn ýkn ýln ýľn ýňn ýón ýön ýřn ýšn ýtn ýťn ýžn ýþn',
    u'žán žän žān źbn žbn zčn źćn žčn žđn žén žėn žēn żèn žfn žģn žhn žin žín žįn žīn żin źjn žjn żjn źkn žkn źln žln žľn źńn '+\
        u'žňn żón žšn žtn žún žůn žün žūn žžn żżn',
    u'ągn ąjn ąpn ççn çgn çpn ęgn ępn gļn gșn įgn įjn įpn jçn jįn jųn ķgn ļgn ļģn ļjn ļļn ļņn ļpn ņgn ņjn ņķn ņņn ņpn pșn şçn '+\
        u'şgn şpn șpn şşn şyn ųjn ųpn yçn yşn',
    u'Bħn Bìn Bîn Bīn Břn',
    u'Càn Căn Cân Cän Cãn Cān Čān Çàn Çãn Cčn Ččn Ċċn Cèn Cên Cën Cėn Cēn Čėn Čēn Çën Ćfn Čfn Ċħn Cín Cìn Cîn Cīn Čín Čīn Cłn '+\
        u'Cňn Čňn Cón Còn Côn Cön Cõn Çón Çòn Çön Çõn Čŕn Cšn Čšn Cún Cůn Cün Cūn Čún Čůn Čūn Çún Çün Cžn',
    u'Dħn Dín Dìn Dîn Dīn Đin Ðín Dŕn Dřn',
    u'Eàn Eăn Eân Eän Eãn Eān Éân Ečn Éčn Ěčn Ėčn Éðn Eên Eën Eēn Éèn Eğn Eħn Eín Eîn Eïn Eīn Ełn Ęłn Eńn Eňn Eñn Ěňn Eón Eòn '+\
        u'Eön Eõn Eøn Eřn Éřn Ěřn Eśn Ešn Éšn Ěšn Ėšn Ęśn Ęšn Ēšn Eún Eůn Eün Eūn Éün Eźn Ežn Eżn Éžn Ězn Ěžn Ėžn Ęźn Ęžn Ężn '+\
        u'Ēžn',
    u'Fán Fàn Făn Fân Fån Fän Fãn Fān Fén Fèn Fên Fën Fėn Fēn Fħn Fín Fīn Fňn Fón Fòn Fön Főn Fõn Fšn Fún Fûn Fůn Fün Fűn Fūn '+\
        u'Fýn',
    u'Gàn Găn Gân Gån Gän Gãn Gān Ġàn Ģān Gén Gèn Gên Gën Gėn Gēn Ģēn Ğfn Ġfn Gġn Ġġn Għn Gín Gìn Gīn Ğin Ġin Ģīn Głn Gón Gòn '+\
        u'Gôn Gön Gőn Gõn Gřn Gšn Gún Gùn Gůn Gün Gűn Gūn Ğün Gýn Gžn Gżn Ġżn',
    u'Hán Hàn Hăn Hân Hån Hän Hãn Hān Hčn Hén Hèn Hên Hën Hėn Hēn Ħġn Ħħn Hín Hìn Hīn Hĺn Hłn Hňn Hón Hòn Hôn Hön Hőn Hõn Hŕn '+\
        u'Hřn Hśn Hšn Hún Hůn Hün Hűn Hūn Hýn Hžn Hżn Ħżn',
    u'Ián Iàn Iân Iån Iän Iãn Iān Íán Íbn Ïbn Ībn Ićn Ičn Iċn Íčn Īčn Ién Ièn Iên Iën Iėn Iēn Íén Įėn Ífn Ïfn Īfn Iğn Iġn Īģn '+\
        u'Iħn Íhn Īhn Iín Iîn Ïïn Iïn Iīn Íin Îin Íjn Ïjn Ījn Íkn Îkn Ïkn Īkn Īķn Iłn Íln Íľn Îln Ïln Īln Īļn Ińn Iňn Iñn Íňn '+\
        u'Íñn Ión Iòn Iôn Iön Iőn Iõn Íon Íón Iřn Ířn Iśn Išn Íšn Įšn Īšn Ítn Íťn Ìtn Îtn Îțn Ïtn Ītn Iún Iùn Iůn Iün Iűn Iūn '+\
        u'Iźn Ižn Iżn Ížn Įžn Īžn Íþn Iğn Iön Jħn Jín Jīn Jłn Jřn',
    u'Kàn Kăn Kân Kån Kän Kān Ķān Kćn Kčn Kċn Kén Kèn Kên Kën Kėn Kēn Ķēn Kħn Kín Kīn Ķīn Kĺn Kłn Kňn Kón Kòn Kôn Kön Kőn Kõn '+\
        u'Køn Kŕn Křn Kśn Kšn Ķšn Kún Kůn Kün Kűn Kūn Ķūn Kýn Kžn Kżn',
    u'Ľbn Ľčn Ľdn Ľhn Ľjn Ľkn Ľňn Ľšn Ľtn Ľún Ľvn Łwn Łyn Ľžn',
    u'Mħn Mín Mìn Mīn Młn Mřn Nħn Nín Nìn Nîn Nīn Ñin Ñín',
    u'Oín Oîn Oïn Oīn Óín Őín Øin Øjn Økn Øln Ořn',
    u'Pán Pàn Păn Pân Pån Pän Pãn Pān Pćn Pčn Pén Pèn Pên Pěn Pën Pėn Pēn Pín Pìn Pîn Pīn Płn Pńn Pňn Pón Pòn Pôn Pön Pőn Põn '+\
        u'Pŕn Přn Pšn Pún Půn Pün Pűn Pūn Pýn Pžn Ràn Răn Rân Rån Rän Rãn Rān Řán Rćn Rčn Rċn Ŕčn Řčn Rén Rèn Rên Rën Rėn Rēn '+\
        u'Rġn Rħn Rín Rìn Rîn Rīn Řin Řín Rłn Rňn Ŕňn Řňn Rón Ròn Rôn Rön Rőn Rõn Røn Rśn Ršn Ŕšn Řšn Rún Rùn Rûn Růn Rün Rűn '+\
        u'Rūn Řůn Rýn Ržn Rżn Ŕžn',
    u'Sán Sàn Săn Sân Sån Sän Sãn Sān Šán Šān Șăn Șân Sčn Śćn Šćn Ščn Sén Sèn Sên Sën Sėn Sēn Šén Šėn Šēn Šģn Sħn Sín Sìn Sîn '+\
        u'Sīn Šín Šīn Słn Sňn Śńn Šňn Són Sòn Sôn Sön Sőn Sõn Şön Sšn Ššn Sún Sùn Sûn Sůn Sün Sűn Sūn Šún Šůn Šün Šūn Şün Sýn '+\
        u'Sžn Šžn',
    u'Tán Tàn Tăn Tân Tån Tän Tãn Tān Ťán Țăn Țân Tčn Tċn Ťčn Tén Tèn Tên Těn Tën Tėn Tēn Tħn Tín Tìn Tîn Tīn Ťjn Ťkn Tĺn Tłn '+\
        u'Ťln Tňn Tón Tòn Tôn Tön Tőn Tõn Tøn Tŕn Třn Tšn Ťšn Tún Tùn Tůn Tün Tűn Tūn Ťůn Týn Tžn',
    u'Uħn Uín Uìn Uîn Uïn Uīn Úin Úín Üín Uřn Úřn Ůřn',
    u'Ván Vàn Văn Vân Vån Vän Vãn Vān Včn Vén Vèn Vên Věn Vën Vėn Vēn Vín Vìn Vīn Vĺn Vňn Vón Vòn Vôn Vön Vőn Võn Vøn Vŕn Vřn '+\
        u'Všn Vún Vůn Vün Vűn Vūn Výn Vžn',
    u'Wán Wàn Wän Wén Wèn Wên Wġn Wħn Wín Wîn Włn Wón Wön Wśn Wün Wżn',
    u'Xán Xàn Xăn Xån Xãn Xén Xèn Xên Xën Xħn Xín Xón Xòn Xôn Xõn Xøn Xún Xůn Xýn',
    u'Yán Yàn Yån Yän Ýan Ýán Ýbn Yćn Yčn Ýcn Ýčn Ýdn Ýðn Yén Yèn Yín Yłn Yńn Yňn Ýňn Yón Yòn Yön Yőn Yøn Ýón Ýön Yřn Ýřn Yśn '+\
        u'Yšn Ýšn Yún Yůn Yün Yűn Yźn Yžn Yżn Ýžn Ýþn',
    u'Zín Zîn Zīn Žín Žīn Złn Żłn Zŕn Zřn Zýn',
    u'Ągn Ąjn Ąpn Ççn Çgn Çpn Çyn Ęgn Ępn Įgn Įjn Įpn Ķgn Ļgn Ļģn Ļjn Ļķn Ļļn Ļņn Ļpn Ņgn Ņģn Ņjn Ņķn Ņņn Ņpn Şçn Şgn Şpn Șpn '+\
        u'Şşn Şyn Ųjn Ųpn'
)

CONTEXT_KERNING = u'ááábáčáéáðáfáháiáíájákáláľáňáñáóářášátáťáþážăbăfăiăjălătățâbâfâğâiâkâlâtâțäääbäčäfäßähäiäjäkäläöätäťàààbàfàhàiàlàtābā'+\
    u'čāfāģāiājākāķālāļāšātāžåååbåfåhåiåjåkålåtćbćfćićjćkćlčáčāčbčččėčēčfčičíčīčjčkčlčľčňčřčščtčúčūčůċċċħċiċjċkċlċtdádădâdädàdādådãdčdéděd'+\
    u'ëdèdēdħdîdìdīdňdôdödòdődõdřdšdüdùdūdůdžďaďáďkďmďnďoďsďtďuďžđiéáéâéåébéčéééèéðéféhéiéjékéléřéšétéüéžěběčěďěhějěkělěňěřěšětěťěžêiêlêtë'+\
    u'bëfëhëiëjëkëlëtėčėiėjėšėtėžèbèfèièjèlètēbēfēģējēkēķēlēļēšētēžðáðíðóðöfáfăfâfäfàfāfåfãféfêfëfėfèfēfħfífīfňfóföfòfőfõfšfúfûfüfűfūfůğbğ'+\
    u'fğiğlğtğüģāģēģīġàġġġiġjġtġżßöháħġħħiáiâiäiàiāiåiãićičiċiđiéiêiëiėièiēiğiġiħiíiîiïiīiňiñióiôiöiòiőiõiřiśišiüiùiūiůiźižiżíáíbíčíéíðífí'+\
    u'híiíjíkílíľíňíñíóíříšítíťíþížîiîkîlîtîțïbïfïïïjïkïlïtìtībīčīfīģīhījīkīķīlīļīšītīžįėįšįžjájăjâjäjàjājåjãjčjċjéjëjėjèjējġjħjíjījňjójôj'+\
    u'öjòjőjõjřjśjšjújüjūjůjžjżlálălâlälàlālålãlčlélêlëlèlēlğlħlîlìlīlńlňlôlölòlőlõlšlülùlūlůlžĺňĺžľaľbľčľdľgľhľjľkľmľnľňľoľrľsľšľtľuľúľvľ'+\
    u'žļāļēļīļķļšļūļžłółtńkňáňhňkňůñáñéñiñíñóóáóbóčóéóðófóhóióíójókólółóňóóóöóśótóþóúóüóźóžóżôbôčôhôjôkôlôľôňôšôtôťôžöäöböðöföğößöhöiöjökö'+\
    u'löööõötőáőbőéőfőhőiőíőjőkőlőóőöőőőtőúőüõbõhõiõjõkõlõõõtřářbřčřhřiřířkřlřňřšřtřůřžśbśćślśńšášāšbšćščšéšėšēšģšhšišíšīšįšjškšķšlšľšļšňš'+\
    u'šštšťšúšüšūšůšžtátătâtätàtātåtãtċtétětêtëtėtètētħtîtìtītňtótôtötòtőtõtřtštütùtūtůtžťaťáťcťčťdťhťjťkťlťmťnťoťpťrťsťšťtťuťůțățâúáúbúčú'+\
    u'ðúfúhúiúíújúkúlúľúňúñúřúšútúťúžûlûtüäübüéüèüfüğüßühüiüíüjükülütüüűbűfűhűiűjűkűlűtūbūčūfūhūjūkūķūlūļūšūtūžůbůčůhůjůkůlůřůtůžýáýbýčýðý'+\
    u'fýhýiýjýkýlýľýňýóýöýřýšýtýťýþýžzčźbźćźjźkźlźńžážäžāžbžčžđžéžėžēžfžģžhžižížīžįžjžkžlžľžňžšžtžúžüžūžůžžżèżiżjżóżżągąjąpçççgçpęgępgļgșį'+\
    u'gįjįpjçjįjųķgļgļģļjļļļņļpņgņjņķņņņppșşçşgşpşşşyșpųjųpyçyşBħBîBìBīBřCăCâCäCàCāCãCčCêCëCėCèCēCíCîCìCīCłCňCóCôCöCòCõCšCúCüCūCůCžĆfČāČčČ'+\
    u'ėČēČfČíČīČňČřČšČúČūČůÇàÇãÇëÇóÇöÇòÇõÇúÇüĊċĊħDħDíDîDìDīDřĐiĐíEăEâEäEàEāEãEčEêEëEēEğEħEíEîEïEīEłEńEňEñEóEöEòEøEõEřEśEšEúEüEūEůEźEžEżÉâÉ'+\
    u'čÉèÉðÉřÉšÉüÉžĚčĚňĚřĚšĚzĚžĖčĖšĖžĒšĒžĘłĘśĘšĘźĘžĘżFáFăFâFäFàFāFåFãFéFêFëFėFèFēFħFíFīFňFóFöFòFőFõFšFúFûFüFűFūFůFýGăGâGäGàGāGåGãGéGêGëGėG'+\
    u'èGēGġGħGíGìGīGłGóGôGöGòGőGõGřGšGúGüGùGűGūGůGýGžGżĞfĞiĞüĢāĢēĢīĠàĠfĠġĠiĠżHáHăHâHäHàHāHåHãHčHéHêHëHėHèHēHíHìHīHĺHłHňHóHôHöHòHőHõHřHśHšH'+\
    u'úHüHűHūHůHýHžHżĦġĦħĦżIáIâIäIàIāIåIãIćIčIċIéIêIëIėIèIēIğIġIħIíIîIïIīIłIńIňIñIóIôIöIòIőIõIřIśIšIúIüIùIűIūIůIźIžIżÍáÍbÍčÍéÍfÍhÍiÍjÍkÍlÍ'+\
    u'ľÍňÍñÍoÍóÍřÍšÍtÍťÍþÍžÎiÎkÎlÎtÎțÏbÏfÏïÏjÏkÏlÏtÌtĪbĪčĪfĪģĪhĪjĪkĪķĪlĪļĪšĪtĪžĮėĮšĮžJħJíJīJłJřKăKâKäKàKāKåKćKčKċKéKêKëKėKèKēKħKíKīKĺKłKňK'+\
    u'óKôKöKòKőKøKõKřKśKšKúKüKűKūKůKýKžKżĶāĶēĶīĶšĶūĽbĽčĽdĽhĽjĽkĽňĽšĽtĽúĽvĽžŁwŁyMħMíMìMīMłMřNħNíNîNìNīÑiÑíOíOîOïOīOřÓíŐíØiØjØkØlPáPăPâPäPàP'+\
    u'āPåPãPćPčPéPěPêPëPėPèPēPíPîPìPīPłPńPňPóPôPöPòPőPõPřPšPúPüPűPūPůPýPžRăRâRäRàRāRåRãRćRčRċRéRêRëRėRèRēRġRħRíRîRìRīRłRňRóRôRöRòRőRøRõRśR'+\
    u'šRúRûRüRùRűRūRůRýRžRżŔčŔňŔšŔžŘáŘčŘiŘíŘňŘšŘůSáSăSâSäSàSāSåSãSčSéSêSëSėSèSēSħSíSîSìSīSłSňSóSôSöSòSőSõSšSúSûSüSùSűSūSůSýSžŚćŚńŠáŠāŠćŠčŠ'+\
    u'éŠėŠēŠģŠíŠīŠňŠšŠúŠüŠūŠůŠžŞöŞüȘăȘâTáTăTâTäTàTāTåTãTčTċTéTěTêTëTėTèTēTħTíTîTìTīTĺTłTňTóTôTöTòTőTøTõTřTšTúTüTùTűTūTůTýTžŤáŤčŤjŤkŤlŤšŤůȚ'+\
    u'ăȚâUħUíUîUïUìUīUřÚiÚíÚřÜíŮřVáVăVâVäVàVāVåVãVčVéVěVêVëVėVèVēVíVìVīVĺVňVóVôVöVòVőVøVõVřVšVúVüVűVūVůVýVžWáWäWàWéWêWèWġWħWíWîWłWóWöWśWüW'+\
    u'żXáXăXàXåXãXéXêXëXèXħXíXóXôXòXøXõXúXůXýYáYäYàYåYćYčYéYèYíYłYńYňYóYöYòYőYøYřYśYšYúYüYűYůYźYžYżÝaÝáÝbÝcÝčÝdÝðÝňÝóÝöÝřÝšÝþÝžZíZîZīZłZřZ'+\
    u'ýŽíŽīŻłĄgĄjĄpÇçÇgÇpÇyĘgĘpĮgĮjĮpĶgĻgĻģĻjĻķĻļĻņĻpŅgŅģŅjŅķŅņŅpŞçŞgŞpŞşŞyȘpŲjŲp'

ALICE_TEXT = """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, “and what is the use of a book,” thought Alice “without pictures or conversations?”
So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, “Oh dear! Oh dear! I shall be late!” (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
In another moment down went Alice after it, never once considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well.
Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled “ORANGE MARMALADE”, but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it.
“Well!” thought Alice to herself, “after such a fall as this, I shall think nothing of tumbling down stairs! How brave they’ll all think me at home! Why, I wouldn’t say anything about it, even if I fell off the top of the house!” (Which was very likely true.)
Down, down, down. Would the fall never come to an end? “I wonder how many miles I’ve fallen by this time?” she said aloud. “I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think—” (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) “—yes, that’s about the right distance—but then I wonder what Latitude or Longitude I’ve got to?” (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)
Presently she began again. “I wonder if I shall fall right through the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think—” (she was rather glad there was no one listening, this time, as it didn’t sound at all the right word) “—but I shall have to ask them what the name of the country is, you know. Please, Ma’am, is this New Zealand or Australia?” (and she tried to curtsey as she spoke—fancy curtseying as you’re falling through the air! Do you think you could manage it?) “And what an ignorant little girl she’ll think me for asking! No, it’ll never do to ask: perhaps I shall see it written up somewhere.”
Down, down, down. There was nothing else to do, so Alice soon began talking again. “Dinah’ll miss me very much to-night, I should think!” (Dinah was the cat.) “I hope they’ll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me! There are no mice in the air, I’m afraid, but you might catch a bat, and that’s very like a mouse, you know. But do cats eat bats, I wonder?” And here Alice began to get rather sleepy, and went on saying to herself, in a dreamy sort of way, “Do cats eat bats? Do cats eat bats?” and sometimes, “Do bats eat cats?” for, you see, as she couldn’t answer either question, it didn’t much matter which way she put it. She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly, “Now, Dinah, tell me the truth: did you ever eat a bat?” when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.
Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner, “Oh my ears and whiskers, how late it’s getting!” She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof.
There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again.
Suddenly she came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them. However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about fifteen inches high: she tried the little golden key in the lock, and to her great delight it fitted!
Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw. How she longed to get out of that dark hall, and wander about among those beds of bright flowers and those cool fountains, but she could not even get her head through the doorway; “and even if my head would go through,” thought poor Alice, “it would be of very little use without my shoulders. Oh, how I wish I could shut up like a telescope! I think I could, if I only knew how to begin.” For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible.
There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it, (“which certainly was not here before,” said Alice,) and round the neck of the bottle was a paper label, with the words “DRINK ME,” beautifully printed on it in large letters.
It was all very well to say “Drink me,” but the wise little Alice was not going to do that in a hurry. “No, I’ll look first,” she said, “and see whether it’s marked ‘poison’ or not”; for she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they would not remember the simple rules their friends had taught them: such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger very deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked “poison,” it is almost certain to disagree with you, sooner or later.
However, this bottle was not marked “poison,” so Alice ventured to taste it, and finding it very nice, (it had, in fact, a sort of mixed flavour of cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off.
"""
