# Description

This is the extension of the PHEME dataset (Zubiaga et al., 2016; Kochkina et al., 2018).

The original dataset includes labels of `verify` and `stance`.

Message-level annotation is supplemented, including `stance_` and `trigger`. Cascades containing a single message and holding more than 60 messages are left out.

The extended dataset is organized in csv format. The table below presents an instance of information cascades and the meaning of related fields. Other meta information can be found from the original dataset with `cid`.

|    cid                    |    mid                    |    pid                    |    time           |    date                      |    content                                                                                                                                             |    verify    |    trigger    |
|---------------------------|---------------------------|---------------------------|-------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|---------------|
|     524965775036387329    |     524965775036387329    |     None                  |     1413996568    |     2014-10-22   16:49:28    |     Hero.   @affanchowdhry: Kevin Vickers, head of security in parliament, being credited   for taking down shooter #Ottawa http://t.co/rVYetE0KYq"    |     1        |     1         |
|     524965775036387329    |     524972195978964993    |     524965775036387329    |     1413998099    |     2014-10-22   17:14:59    |     @LindaFrum   @LeBlancJpl @affanchowdhry good for Vickers                                                                                           |     1        |     0         |
|     524965775036387329    |     524974387125317633    |     524965775036387329    |     1413998622    |     2014-10-22   17:23:42    |     @LindaFrum   @affanchowdhry absolutely!                                                                                                            |     1        |     0         |
|     524965775036387329    |     525005729938554882    |     524965775036387329    |     1414006094    |     2014-10-22   19:28:14    |     @LindaFrum   @affanchowdhry The real hero is the soldier who lost his life doing his job   and serving his country.                                |     1        |     1         |
|     524965775036387329    |     525015279387299840    |     524965775036387329    |     1414008371    |     2014-10-22   20:06:11    |     @LindaFrum   @affanchowdhry.. This was an attack on all Canadians whatever stripe   Obviously these despicable acts are from cowardly cretins.     |     1        |     0         |

| Field          | Meaning                                                                                                                    |
|----------------|----------------------------------------------------------------------------------------------------------------------------|
|     cid        |     ID of the cascade                                                                                                      |
|     mid        |     ID of the message                                                                                                      |
|     pid        |     ID of the parent   message (where the message is repost from)                                                             |
|     time       |     Posting time of   the message                                                                                          |
|     date       |     Posting date of   the message                                                                                          |
|     content    |     The content of   the message                                                                                           |
|     verify     |     The verification   label for the cascade (0-false 1-true 2-unverified)                                                 |
|     trigger    |     The trigger label   for the message (0-null 1-amplify 2-deny 3-clarify)                                                |
| stance         | The stance label for message (from the original dataset,   -1-unannotated 0-support 1-comment 2-deny 3-query)              |
| stance_        | The stance label for message (supplemented, 0-null 1-negative   2-query 3-support 4-positive 5-social influence 6-pitiful) |


# References
If you use our dataset for the task of **Trigger Identification**, please cite our paper **A Progressive Framework for Role-Aware Rumor Resolution**.
