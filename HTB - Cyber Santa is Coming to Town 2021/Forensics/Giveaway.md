![image](https://user-images.githubusercontent.com/80063008/144764376-a577ab71-04f7-4488-95cc-42957085bdf6.png)

We were provided a .docm file and generally, the first thing I do with such files, is run olevba to see what macro's are hiding.

```bash
olevba christmas_giveaway.docm --deobf
```

In the output, I found this part which to me was interesting. The link drew my eyes and then I stared a bit at the obfuscated charcode.

Dim strFileURL, HPkXUcxLcAoMHOlj, cxPZSGdIQDAdRVpziKf, fqtSMHFlkYeyLfs, ehPsgfAcWaYrJm, FVpHoEqBKnhPO As String

    HPkXUcxLcAoMHOlj = "https://elvesfactory/" & Chr(Asc("H")) & Chr(84) & Chr(Asc("B")) & "" & Chr(123) & "" & Chr(84) & Chr(Asc("h")) & "1" & Chr(125 - 10) & Chr(Asc("_")) & "1s" & Chr(95) & "4"
     cxPZSGdIQDAdRVpziKf = "_" & Replace("present", "e", "3") & Chr(85 + 10)
     fqtSMHFlkYeyLfs = Replace("everybody", "e", "3")
     fqtSMHFlkYeyLfs = Replace(fqtSMHFlkYeyLfs, "o", "0") & "_"
     ehPsgfAcWaYrJm = Chr(Asc("w")) & "4" & Chr(110) & "t" & Chr(115) & "_" & Chr(Asc("f")) & "0" & Chr(121 - 7) & Chr(95)
     FVpHoEqBKnhPO = Replace("christmas", "i", "1")
     FVpHoEqBKnhPO = Replace(FVpHoEqBKnhPO, "a", "4") & Chr(119 + 6)

A close look can reveal that the flag is broken up in pieces across these variables. I manually decoded the charcodes using cyberchef one at a time. I'm sure there are easier ways but it took my 10ish minutes so I can't complaint.

HTB{Th1s_1s_4_pr3s3nt_3v3ryb0dy_w4nts_f0r_chr1stm4s}
