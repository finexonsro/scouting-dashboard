import streamlit as st
import pandas as pd
import numpy as np
import base64

st.set_page_config(
    page_title="Jahn Regensburg · Scouting",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAABWGlDQ1BJQ0MgUHJvZmlsZQAAeJx9kLFLw1AQxr9WpaB1EB0cHDKJQ5SSCro4tBVEcQhVweqUvqapkMZHkiIFN/+Bgv+BCs5uFoc6OjgIopPo5uSk4KLleS+JpCJ6j+N+fO+74zggOW5wbvcDqDu+W1zKK5ulLSX1jAS9IAzm8Zyur0r+rj/j/T703k7LWb///43Biukxqp+UGcZdH0ioxPqezyXvE4+5tBRxS7IV8onkcsjngWe9WCC+JlZYzagQvxCr5R7d6uG63WDRDnL7tOlsrMk5lBNYxA48cNgw0IQCHdk//LOBv4BdcjfhUp+FGnzqyZEiJ5jEy3DAMAOVWEOGUpN3ju53F91PjbWDJ2ChI4S4iLWVDnA2Rydrx9rUPDAyBFy1ueEagdRHmaxWgddTYLgEjN5Qz7ZXzWrh9uk8MPAoxNskkDoEui0hPo6E6B5T8wNw6XwBA6diE8HYWhMAACepSURBVHic7Z15eB3Flfbfqu6rXd53AzYGs9gOBhzAYYlsJsEE+CaQiUwSCCSYMAwBBgJxZtiuhR1gEhgCmcCYZUgcY0DCYfPGYmS8YLyAd3m3LFmSZe277r3dVe/3R3dLV7K8yLZsN/TvefqRbm9VXXX6VJ1Tp6qBgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAo0Cc6AwcIYJ0/smZmCkP96LM7GwNAFOmTBEj8/I6fPbM7GyNKVNETl6e2DRiBKdMmULvd/vjAJA5YgS9/zeNGEEAiL93/PH2ePfPmThRbhoxglOysggCEMCUcLglj5nZ2RrCvQWJnIkTZZv9JIRznIdbFgEBAfCpBlwNhMYA4iMgVDj69JFCScMQglGyzfOYAOy4/8/fuHPd5nP6dI8KM0GE0gdQa+kctyGFTWmaolt95Y76hF59bVOmp0fr9/Suqawt7Dv4jISQmRqJKbtnQ9We5u49BlpGKMmwQ7SpmiiMlFSTQtZVFVmJZqKR2K1voy0oSaG13cwEFTKEYWob1DSFCQAIIWRHK5MbKivqevQZpu1I3aVbSnaXA7IvoL8c1nOA2b3b4GYA3coLto4oQgMArBuY1s3u3X+4BWBAXcWWoYW1jQmAGA4o0fq4vsFXAsjsbENMnKjqFn/yevrIb33Xqm8QVn3dYBH/GAdphMzu3ffazc2pWtEUykoRwjmfICAAAQGRlFwda27qbkJIJCbUh5KSG5prqgcmSAmlCSMpudaONnc3hQABWJowhYABQIVCjdpWZghMVM4tYWsNKQApBEhCCMPJoxCwBa2E1JRau6GhjxbCSuneYx9JIYRgpLGhp2nbqRqETEmvMM1QBELCijSnMNrYS2hApqVVGAmhRiMl2WjcuH5xWsb3bvLKqEsr4hjiLwEkDSGEatiS92nq2eeOd3fHOnGLBDjVTxxYWyS4xzSAEFw5cn8LtCpWT9Slewzu+RpAvAAIHPi1MNzNcu9jxB2ju9/LUzyx9vubtuflpp418kqvjA6Q3kmHeaIzcCRQ2zEAGpoSUrSvnEMh3O1g17Uvl/a/Qwe51hOqztDR/Q6Wx9b9GoCEhmZnXsSTBl8KIIRUAGQ0f1dubOumBTIhTSJG3aKLOvqLTh6L51jcq7P5wkH2AZDCkDrapOW5w69OHj58PLThneEr/CSAAk41mI0Vlf3SAIREaHHStT/8wwnO1wnF3rYtGcB4LfwpgIftQzsJIJz82inde1a4+1KYm2uS9NNzHBNISubmmkKHUgEA/un2tcFPGrAFaRpO51xqiPHj7eIXXrqibsmS3ykttaB2hNF16Lb87WhfR8c64kjvdaTneyZLB/skhDZMLUtefvm/Bt9xxxJr+05Xi/hSAfpOAAnAaKqp6ZMKAIoGAOjeKRekX375tSc0Z8eZqrLyjwAsAYUrf/SVR8PDTwLo6QHDam5Kjz+gjaQItFZaShtKmTB8WReHhYS0oWEalJH4/YYZ8p0TGvCXAHp9QJXULb0KiDMMtRaQ0pAAacivsfgBAAgJQxnOY2pqAQBN9bU94ZSPr8aD/SSAQhiGBpBYW1Z2ei8AcAu/rRvtay5+LoZ2jQ636W3Yt28ogJAwjCgO7vw+qfCl9SikccDm5pshfvsjzQOXycmMnzRgCxSH3+EmCUH6Qhu0h0IIIQ7vUcnACDluyE54HIQQwOHW4kmGLzPdSXwpgIfXcXAcaNHCPbCqaiLSkCC1TypVgFrD7NvXSBw8MAQSOOQ75I8na48vBVAcVv9a2ADMyK6tf1h+66Q/9T7nHLO5sNAX/aTk004zK7dssTPeeut2DB74uBbCloesK1/2MvwpgJ1527sPG7n7B4WFe1FcDCifDFdt3w4oBfYbWHWis9LV+FQAO/G2R+sS3Q56fID0yY6T183bQ8Dh9Tj8qf/8KoCdGvaUFEKQTqixL+rJyys3byPQcYTY1wU/PhfRKUHy4yN2HuFTI8R3tTMCSNBKHSwiOcBH+EYAw67xOxboZkUjaQB8GwHSNfiid7EfvhFAjyhAQf/lO6BjfGOEZAGkVmKSEA0pPXsVAhgljaMPQ2c4LDFypMgBkHn02TwsWtLKzNTHzjDyZ2PgGwH0+D8gkqW1CbSGIh0NIivLn6HEHm5b4E/x85kACsMgAEnb7uxUzP3wJoCX/elPw5MHDx4cjbEpJISwDn3p0UOyd5/uApZVIK67rtTLy1Hd8ljl7TjjJwEklZJCCDupe/cyAMMg5NGUuwSgEkaf/2zaFZdfm9bQBJjHqThsG0hLQdPadbMA3OTl5fgkfnLhJwH0AlKTGqsqTu0LxAWkHjlMTwMMQ6N7ukLnJ5QfKQqAEaPudZzSO2nxkwB6GjDWfeAp2wAMloZ5GP23QxjMlgBIqbSmEFIKQRxuuGH85DUAoABE+50doLWmlFIK8OiHBt0S8GnIo6/cGV6YuYw1NXQDAOjD0YCUJE0AJsmWzfuNEAWEgCEEKAlqSQWhlBTqUH8JZ9MQCqCiJikEKIUTPnXI7djZDj4NefSVAHoIbevD1txKNTcJIWwhRMT9621RIYRtW9EoAGg4zkVpQBgShgEYh/orZesGKQ1pSCGEVlrZGj7VSMcbXzXB8AyHlOQ64JAxCRIAmpT4VUPu52chyZDQ1C1XhQyhozZln36jCQCkEDDQVJBfX7t23XJhGEIcQooIx5o2TAM9hwyHZcgxKWcM62U4xoxyV6o6qof+uuMnAfSaYDPW1NwNOKT6liCQPnLEGABjDnaiZmu8iVVeuXPQ9TdMOJIMzu4/rN95jz44YcAlF9yV9u2xY4UQGloJeDNFD7b6wjcUPwlgK97yG4fCqWyNgytLQwoptHBOETJkkDRwBFMbhRBluPuuvwN4vfTVVx/uc/V1j4tB/bRUNmgYx7bT147ACOl6WhYnSu3dZy8AQB6WH1DCedEOtLWVCYLuAo9KCNGpjYDIDYdNkhgwadLUor/NuAX7yiQMk1Q8Bk6jA+PXpt5PAiiEYSgACdXFhWcDgFb2SZV/AXB8VpYNIbhx48aEoQ/99u+Vi5f+CpYlCUnJLvQ1BxrwuCG05vFyGB8RAuCoUaNi5OpQv4n/8kr9V6sWGAYkCdVlY2b+VIC+EkBSKQkg1q1//10AcJRDcUeWiexsg7m5Zm44bDLs/j3QpPCcXZqkKJk7Z5qqrNSQhiCDWLJ4/GiECBWNJZ2wxNusQJ/l/skCSSmE0O3PJSnPmfrksvoJ/7w87bLelwFUX+c5Hp3FjwII6fQFjytexMrerKzx5qBBA5sbokwwEmAblm6Yn71QCFHBcFjuF961aJEkyYqZOX9Pu2zsZZCShzeC883ATwLYsl6oFYmkAsddi0gAqtcN//x4wrfOvxzRGCBMwABiE67aVzTuvZvEgw8u3E8TjhunhBDc/pvfzOs+4crmUN/eyaBvpod2Ob5qCYRh8GIgNVJf2w84NgGpnc5D7/61AGwkJkSRIG0YMpZwxpn9e1591VtrfnhrDymlZpxJ4E4JFTP/+7+LVW3tbgCQwqfr6XYBvhFAb1LSBUAvKxp1Vkg9EZOSbG0AMLXSJkgTZAIAK2Xkt3oPmnjVz0gCubntrXSZBWjC3uj86gpb2J+tum8EMAsgBBABIsIwnI+yyBM40VygJapFQ0sATD57xBUAgHHjOjobjTW1jQCgu6DYg5GQLsbTgKlAGmNWMoCTZlqmdBbdEkZiyohMJ6hVsQOVpBoau6y8fToQ4h8B9DTgUmBvQlpaJYATqwE7QGurdz1gigMMEVKxdXQ6AIC/rGAvIjqS0qNXMYDBJ8IR3SJbEgA1KCS0BA0SpjR2LABi1Ho/nyAAkdC9h2q5NgCAv4rCmxNixBobewA4JnNCOo2bpLNKq/MRN8NdryZSW74RrUETba4CwMSkhGHOtcc+3z7tAvpKA3oIpWKJJy55TWhNTU1oZwFqYZhEc1TUfbX6XQBATk6LOJAUQkq9JiOjh5medq67+5gLoF/7gL4TwIGAgRP5bbiQGYKUQkJ6ZScAyIZVX+QMufc3n7iO6NaRmpwcSVLvuf7HlyT2H9gXgNakPOYPQH/6YXwjgAQApcSvheimraOfmN5pcnIAAHr79nIjZpXasWYFIYW2LBkt2rNg189vvdv9aGLbxjAzUwiA1aNG34CkBGhAd0XwnvvpCt81xL4RQG8c7gWg/NGePUsA9JfH0QjxghB2Z2T8cjgg97r7ywDxbaDJOal9bCsEAFWYOTY5ZfjQGwBAai31MRQUb32c3kOGbAYQo1LBF9O7iJbOvZmY3AScGG/GWUC07R4BUksIQdFesHJzDSGEXfnuu3cnDDmlnwKUlMKQ+thFpnrDkZH6+m7w4ae6/GgFm02VFYMBnBArmM7c87iNQgih2wsfw2GJceP0irsyB6SOufB3GoICWggc24Fg6ZaA1dycPsJRKL6a+uQrDej6Aa30AQPzAQw9vJURji37abkOYHa2gcxMCCFU3eLFMxJPObW3rZUypTzmkdzaDYaN1tf3HAOkA/DVyvq+0oDwvhdcXdUPwGGujHBs6WiIrT1i4kQlhFDVubnPpV9xxfc1oAwhjS5RTC2fDBWiEIi6K4j5Bj9pwBakYZ6weLqDaUACAiMyQ+W/Hvud9IvGTU666MJrbGhlUhhd7qgT4GdArGsTOfb4SQO2QKpjtkBlp9IFxN7z+qce+ASipHqp2e3bl2UnXXThNbbWtqGOg/C14pu+n4cfBZBGKBQBgOPlhvGa3RU33ZQe+uUjf3BruaPKNgbv3dsUjVh/BEAh5fFb8M2njmg/CaBn3VFIZ07IcbVAhMD8NWsi8oILJlZ+uPC7JB1joy2KpPjqsbtfie4pKjcAQzjrfnQ50jAt+MwFA/hLAD03TKixpmoQgDg3THwdd10dZOXl2aF+3RKTBvR9WAhBZLZd1txdZtcY/9m6Gjtv8/MABGRnPi7bGZzbSjckLSE5tRaAplK+0oR+EkAPGs7bftwZAZgwzeqkM4ZdtfXBB8+XUqrszMwOtWDp9Bdfju3a2QjAgNJd8FY4vmztBuXGYk1p8GF9+i7DAEDVzviwYge2TElAOxEsHW2dDWVnlEqkpqLX+H96iCQys7PbHHe1oDzznXfKGtZt+isAAUMe0ciHOpiRFVNOxl1PdCiUWAcfhrr6TACdwrZirsAlhDQA2A0NB+zqCyEAKcWBts7GBVDTBIlu5424fts9t5wBQDMcbluOU6aQpNg+L+eZaNGeCAADugMtaB98lS/jIPOfY/W1zpc0Q04Z1FdU9AdgCMP0VT/QXwLoyopqakgCgIaCwnMAwDDsOmjtnNEaiQcAaNqdz/oVy+3GVavbbqu/tBuWr7Aje/Z4bZlzmXHwMH9hOBOREk45LdT3up/cI4Qgxo1rU44iK0tj0SJj7Csz86O7C54HIGwpFUg3V47aTe7VK6/tk7Ul2hhJB+Iric65ikhKTS8GACsSTQMAu7nJOPCdTl785IgmbVsKIeyUPv1XAfhnLZAOAL1PO20rYjEgKUl6xrLWQkkJo3r79vfWTvzhfT3OGGlGi4tbHNiJgweb0U2b7JFv/+PBpFNPvVtKYQNICKWnhdyJRQdozlqmdTBtxOif5f3811MxblzVft/6WLRIkxRbJk95LnnYGfeGBg1M1FQUwhResxmrr2842AM3VFWMbBN56zyahGWh5ymnFAJAU1nZOcnnDoc0zUK48dp+UoF+EkDADW+yqGoBILnfgAgA7Fq3Toy66FLqpCRnehoA6c69HXjW6OpTaiIFWLu27RfTy8oArVEOvQEAvFVMRWLikLuuuaavEKLDD8h4PyRgyVMG9e3346v/VQjxBHPZ5oPYIitLc8oU49w/ZpVUXnnx270GDbxZSdMOkSaFo9Mi+/aVAQAWLerwYbudPrRjYyvWzKI1awynDPpbAJDav/8GAJa27SAcq6tpyM8/BQBEQkJvAMaoQUN2QBrVEugFgu5CpE6YEhuHAQK0bWPKlCktwjQF4+QULNK6pmETojaRaBoa0El9+6ac+aMfnYt580qRk3PgD8goJWEYTD3nrHtzR49+AeNQu5/Aun3BwilTwt0v+vYNRu9+KdCK0jAlLRsyGl0LACgvb6+0nGWrkxN6A4DWWkgpHYtKCAGJymGDBu0EIBJ6piUCQPm2zWcedcEGHBx36Vys+q9pfyfJ+l27SjKBhNwhQ5KaCwpLSVLZtiZJpZQmycatW0pzR/RNaz8cFnYNh7V33tmvuai4iSRtxRhJVsyb9zQgwNxcE3BHQoTACCChblNeIUnSthVJiySLZ826D0DL+R3luXLx4tfc/FkkGSkpbVz7wAP94vPSghBYjTGhph078uk+TPwzNeXnV7w/cGBKBmA2FBQUkuTnTz/xRnx6AV1ArlvBa55+8tckGdtb2rTxrrvOBCCiO/NXuZVlO3+pSTJaXBJde/vNpwPOBKG42wnvd2TLti9ITctSMZKM5G1eGwakd7yNAOZtLvSEwnaEUDfmbdiSDSS4IfltJN39Jglql674X0du7Sip2bx1y6q4PIm48wUALL/11qGRopJI/LMoVxCbtm7dmAkY+Q8+OMCuqKgmyY/v//UM93pfCaCvrOBx5S8QAOpqa3arSJShbunJvUeP6Q2AtGPOopXexF3nc0cqoW/v0ICLLj0DANwm1YPwRmrrGuYDAkI6fczEIaeN/vkf/zgBQEfDbS1XSyklAJ1y1tlnf/e1lzKFEDo3bl0YLyR/2003dUs+ddBEADAMZ/3zaEX5Yvc0A/F2g5vH/hdfeFZiv96JAJT36SbpjqoIITbmACp9+PAhRnJKD0RjVAq57vWdLdYTiq8E0CvbfTu3lsZqKhRSUiD79D4bAKzaynwgznQVrvIKJQhzwOCLAAB9+4q293OmT9asXf2hbmqgIaUEFJGSgoFXZNzbfrhtZPzFAk5MtFaAEWL3i75zNwAxbty4VuvZCcln/5/+YlLotFN6asdIMXVTI7F951tuJtr2/5w8irTBZ45CKAG6gzADu6ZiNwCo9B7nICUZdlUFK3fm7QOARX/5i88cMT4i7L4w4ZSUAWUbvqoiyar5Hz8NAFXvzr2FDhZbsUiydsln8wGA+0/nFEJKvAYk1X25soikVratbFKp+npdMH36VYDbtxMCme2aYE1NpZ3uGZsjLJ3+6veEEM4yvuGwJGms+WFGj2j+7nKS2la2pUnWf7W2KBdIEo413L7JNgCgbtWGmc6Naen2z/PuB7cAQMW8+U+TZMWG9ZVTB/U8FRAtZeQXfJXZLIAkxd6mpspYXeNOADB7dRsBACwq/lJXV9twvgHnXKCdkYZQ735jPux/XqpwmrD4CqdeuND8JRCJFhT+DwAhDUMLpSDT0tD30kv+9uF55/XDuHGKbvS15+l2FgEUEEJCQxNJiUgafc4jJIHMTGLKFEMIoc5+6KlpCUOH9LGhtSENCABWYdH/jAci+lPlzeHwEEJKNaN//1QjLeFKAJDQUhDQjqPc1NW1tl2090sACPXsMQoA7ObmzetLqitILbP85Qb0HS2Gw+Y3Zr5DkpFtO7dvBBKmjxkTim7ftcfVFIokqd2+e309d/3X7zOA/ft0JAVJsf7ay3tGduaXOYZqTCvbMWbqlnw6F4AQponwmDEp9Zu2FLrWrGrRS046tl1dzU1Tw9/1NG3Zy3+9n80RKtJWVkyRVNH8gvL1117b00u3TV7cvO3KysrQdbWu+aGpHdtKkWRsZ/4eAkY2kNywaWMxSebPn/uK+yy+MkB8iVfICx9+4GWSVBVV1q4nnxwNAPXLVs53RcL2ZEO5zVb1R4uecK/f31XiOJFRMWfePe7FllI2qZxr6z5fMivD9ZnWbd20hy0C0do4eunUL1vxNgBUvPH2L+gYqLZSquVepf9495GD5kMIVC+Y9wRJrUiL2knFdq37upUr5wNAafgP56mKyhhJrnz6D+H4sgnoQnLDYRMA/nrd98J2dRVJsnx29l0CQFlOzkPxfSWn4hzNEdmyc30mYJAUHUwsEiSNeUBic96WNSS1UratadN2hblp/ablq++8fULNunUFJKks1aoBHQEhtaZVUtZQNm/ua6yroyN2yr0NdfO2vDUbHXeN0T4PdLV7JmA0b8xb7wi5chwwulXAK96Z/RAAlL+ZfRdJWlWVOvuGq++KL5uALsTpZAvcm5R0Wumq1dUk2bjsi5kAsO2Rxy+wysod2VPKWULIVlSkUg0N3Pvq9EsIiI5cK84+gc0PTZ7A0n0kGaNta61I23aadLuwkM37Km1NUisdp//cJElq1wbSJJWtaDmKy2J5BTc/+ugEiI5dO8zONgiIvc8+e4murSdJpbV3I0cMrfIK5j/+5AUA0PD5F38nybrtO3c8ByT6dnUiv0FACGkgA+ix9tXpe0iyKW9z0drvfz81FzAb1ny1hVpT2bbSbFFSTvO48ouXgAM3VZ5glM2ceS9jNhVp2batVUuTyzZa7yDYWtm0beU0o7EYS1597dH4NPZL281TzedfvESSiqrFmnc0oWb9mg1bwoC59rzzUps2bS4iyc0z/7bpaiBRGEHre9zwhrw+m/bo8yQ1GxvU3pdfHgcAtbm5WU4F0lKeLeK0ljpWsrfxy9tuG0JS7BfD593bFYT6eZ887vbxLNu2HVNAac/gODha0XI8LjZJVv7jnefi871fmo7LRiy77bYh0aKSRpJax7XwLf3Y3I+zAGDPX14ZrxrqNUl+/O/3zIHTfPvKo+FrcsMZJgC8dOWFv4juySdJ1i39/GkA2P3icyNi1ZUW3WY4Tiwskqx8/4PngdZhvQ4QnlFSPnv2NNY3OirNpqXa3q9DlLK1Uq72qqtn+XvvTQNajI4O20kvL2Vvf/B8vMB54kxSW5XV1u4XnxsBADWLPv8jSTaXFMX+cfXVGQDQwdSAgK6CzmQfZAJ9d859r1hrzcZtO3ZuzMxMAIDGNeuWkKSybTtOMrQiVaxwT/2GW245gwfRgkCrttr91B/vbtq4rilOIGxvU0ppVyjtuI0k2bw5r7bk+edvAQ5unXraL++mmwZGCwrqFamVsuL1rE2SDWvXLQWA3IyMHnXr1u3VWnPH3Hf2jgV6ubFnQSfweOI1OV8+84fpJDWbIyx49ukbGQ7LipnZk2i3WrCeGmmxJOfNeR04cJMYl4YBAGsm/MvIxvkfTY/l7647lAa0duXX1c/9cPqX11wzJP4eB0zDzUPV/A//z9V+Tp61pnIMG5u2Ztkb2ZMYDss9r7x2LSPNJMnPHntorhs0ETS/x5vcjAwTgHgt4zs/iRbmkyRrPlvyHgCsvu66lMi2bUV0TFPV0o4pm4q0rcpyvXv6ny8EDhJs4BJ/vOiHN55aPWfOpMYVK2ep/KJF1StX19WtWVvKwuJPGpavnFX33rxJRTfeeGpH1x7s3sX//ecL7YoqR9u5rbzWynP16Nj2/D2rr7suBQBqly6eTVJHdu/Wr15xxaS4sgg4ntAdx70USN88O3s7SR3bW9a4dfLkcwGg6t33H/aUkucw1lrTspUbQpW3MRtIJmnwQJ9b9dJyx3Xb738O6PsU0H2/80ljvxi//c8RJI1sILnxqw0bSWov3KpVZ7sa+4MPHgWArZMfOTdWXNJEkrsWfPAlWkPAAk4EXuG/+8ufzmDUCZ2rmbfgGQBY/dPr+jTv2FXuaEGnYm06wwuKjnOu5r15jltm9erQ4aQXDoclc3NNV2idihcC7m+DubnmoQSvJe9umhXvzXmJdJyO8U25spUmqaI7t1Ut+9GPhgBAzZyPniFJHWnm0mmP3+6WQWB8nCgcy48iPLD79eXLFjeQ1JGdu6o2ZmYOAICy7Lcfa9GC2tGAWpO21k5/sLGRla+/+RPg8IUwHm+Ryk5f56ZV9vqMn7ChkTZp6f2Unzt0l/2PxwBgRWbmgOjOXZUkdenSxY3/0a3bmRACBzOkAo4DrgYwlmSF3/RqrnzB3KkA8PnYscmRLdu2k9S2sto4kT3r1a6qqsuf/sx44MiEsNP5ne6ksee558bblZV1Tr/P6/g5gx6u01tHtmzd/vnYsckAUL5g3lQv74v+Y3Ku++yB8J1owmFICIHnzjnj9qovV5Okju0pqdh4x72nQQgUvzLjeiciRdnxTmRNUlnO/JFoUUHdrqkPXwUAq7tQCL1773o4fFUsv7COJG13Dgu1o/KUtp28NkdY+tqM6yEENt5xx2nR4pIKkrr6q1Xq2XOH/QBCBL6/k4Vstx+0+LHHFtI1I8tmz37XO16z4KOPnT6gio+SIbUXqkJG8vOju5544kbA0arHsmmLN2IKpk69MbqjMOpoYbutVqaiFwZWs2DBx971lQvmznBPsT99ZPJKN4+B9jtZyM7MNBgOyydO7XvVvuVLNEnLKi9TW8L/cbWQEpt+dtuQyLYdlV4dezpQa9LRN45lrPbuY9lbOfd793UNjiN28JIU8b7Gslmz7ld7S0hSW66V0UYlOzGGqnnntspNt/1siJAS2x98+Gq7rFyRtMq+WMrfnzbon0iKQPudZGQ7PjVj4eQHX3QNSt24ftOabHfiUfGLL97AhjoqMqbdMV3tVbwmbWU7vmqlWLd06Zwtt999undv5uaaXrTKofLhRdswzjpde/vtp9ctWTzHVcDKmzqqqR2znC3j1THWN7D41RdvAIBswGhau34NSU3b5vx778gZCySHw/vPvgs4wWQDBqTE/SYu3v72mxbpzPEte/f9p7xzSmbN+rPb1MW8/mBbLdTqe4sVFFc2LfzoweVXXtI/Ph2SjivGE8rsbKPlNynjw6I2ZmQMaPoo98Honj2VbgptrV1XJTujHk5+S95888/e9WX/ePcpr+ktmP/B3scTcA15eC9CwAnAG1l49Z8u/5PtNHURu6yChdOemgAA9wCJlQsWfOhUvG1RO+HG8UKotaatrJa+YnTr9n318+a9WJD16PfnAD0PlYdsILng0azvV77z/l8jW7ZVtQiaHbP3i2VwhmdId0J8fe7it+8BEgFgV9a0CWpfBUlG7dK9fOv6a28DWjR9wMmIF1V8AzBw4QP3NHp137x5S+nam2/uBynxPpBSu2TpSqcttKx2UaWtitCJ5Wt1DldWsmH1V/vK3p+XWz77g2kFT/9paslfZ/6g6p35V+x+5tnHat/5YGrlRws/iKzfuIsVLXJHi7Rjtq21Vi0hq63yp2m5cX91ny9ZOQNIhZRYe8PN/ZryNpfS9Z3nPjZ5B4AkkjLQfic52ZmZBqTE4326/ST/vZwo3aat4cuvltwDJArTxMdjhnVvWL/+M0/JMa5Z1K5geIKonIBUS3UUjBqNkRFrv90klaJtK8vWTgyhckXPC3Fmm2a3ceWq1R+fc05vmAYyADOyfpM3tyW24/0c9XDf9EuFlIHbxS94FTX9O+f/e/2WLY6Qkaxbtux1AIBpIrtnz+61S5d/TLrBq55hcICIP+1EWXuhV5a7eVHSFp0AWJtUyjMs4q91xK9lhpv2InPqli37+Av06iZME2EgoXbRomz3suaGbVv5v98d8zsACAfzPXyF8Cbo5Pzsx2+zpkaRbCbJ6jnz/wYgBKfCkyoXfPQKLctVW5ZN3WZI9uDog0hsHDZJTZvUNm3ljvlaNsvfnftWGEiSpuP7rl2w4GX3kibW1vHtX/zkbwCwevodXT5CE3CM8RYX+ikwfN6dk0poWZquJizLmfMOAClMR6mUzZxxb6ywoMEVFrttVMrRo7V25nUop09p7dlTXzZjxr1w5xsDkJVzFvzVbeWjtKJ60eT7F04ABpIUflvtIMAlMxMGhMR/hvCzTx960AuGiZBkXW7u+x8CqV6fvvDee0fVf/7FZ7RbNJqtlFL6cOaAHFjyqBwvtxtkqli/fOVnOx64d5STQ4EZQGr1p5++T5K284Lo3Mcml90MjHKjvoN+n5/JzMw0AIn7DFy15PePRVzRiJJk87oNq9b/27+NiTvd3PfGGz9v3rR5A1tdJtqZqK5sZdua7vxfz57wenZatwicdof8nHkpJKlsNm/esqF85syfI25R0M233z6mad2GVW46EZJcMu0R6z7gyo3hcEKg+b4mTB8zJgQIPGrizmVZ/1nrjpTESLJpx45I4f9NvwtxmmYMENr9yku/qluxYrVdVNJerykVZ3iwxQBpMUhasItK2fjFitXFL730qzFAfD/OKHjuz7+L7NjR+kJoi8uenLptWoq8g0cx/BdwkuIJ4X3AlZ/c9+u9qrpWkYw64TAWqz7O/XTD3XePbneZ3Dp58sXls9+cFlnx5VI7b0cVyyrISHT/5rbZIisqaW3ZUhX5YvXS2pzZ03ZOfuhitNNiX939r6OrPl74KaOWJ60xu6pOf/Lb32y/D7gMEPuvmBrw9WD6mDEhCIGHJX45+4arqxvz8kjS9iaBRwqKYmXz576w5sYbh3Z0/fpRo/rveOCBK5tnZ19ZMv2FR6ten/VU1euzniqa/vKj9bMXXrnl4alXrr9kVP+Orl1+4w+Hls6f+0KkoDBGtkyQshu3buYb//KD0p8D50IITB+DwOL9OpOdCYOk8Shw2Uvnj/pk66xZrjy09vqixUXV9UuWvLzv2WcnZANpR5wWkLbv2WcnNC5e/nK0uLiaLZ1C2qTSm2fN5F++fc6Ke4ALICXCPl00PuBIkE4r92TP1GkLfnUrqzZt8NpVr19G1tUxtm79roaFC18sfOkvk/Juv3NsNtA9DCS1u5sZBpKyge55t94+tuz5lyZFPv70xdj69btYV9+moSapKzes55w7J1VkJeCGq4FECOm7hSWPFd/Yzm4YkFNIIidHTp448fJTRw25+8Ibb7nh4psnGaGhQwDAUoBheIJhKaCkFM3RphK7uFRpyy5K7NVrJ4RGY2nJ6FBKWo+EwYOMpITEQRg0GEhosWkU3KV5VUGh8fnf/6bW57y2MX99/q+egVglBPAYKbN8+J23gKPHeQGdECr5W2D8S9/51txPH/ttpHzVMrojJJaruaKMD044MMo9N0LSoqVY89VXXPLQ7/jK5WOm3w+MzwBMt8n9xsf1faMf3iMTMHKEUIAAqHEnMGr4qQP/35DLv/PT0y+77FunXHIp+g07C+jRy9OHyt285XC9Ty2YUBCsqUTFzm0oWbUceZ8v212yasWC0u3F7zwNfOTFC4YDrQcgEMA2hAE5JRyGmDpVQ2vcAQzsBXwr/bS+5w8+e8T30oeeNrT/mWfVmGbooj59+wGmAYKAZaOxsgo1NdWF5bt3hOr3Fm+q2bW7tHZnyTvLgIWfALUQAtk//rGRk5ODnAN9fekbSCCAHRAGJMJhZD3+uPa0okvCWCDtMmBUjxCGaIlUO4p9dBpxJgGJFcDqZ4EdAJy9QiB8xRXmyM8+48RA8AI6AwGRnQkjnJHhhNtLCUgDEF7Xrd0mJCAkwqTMzsw0sjMRhM8fgqBwOocggBxAbsrIcMvus7ZnfAYd9O0CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICjpL/DwEm3lHx1bzsAAAAAElFTkSuQmCC"

JAHN_RED   = "#C8102E"
JAHN_DARK  = "#0A0A0D"
JAHN_CARD  = "#111115"
JAHN_BORDER= "#1E1E24"
JAHN_MID   = "#1A1A20"
JAHN_TEXT  = "#F0F0F0"
JAHN_MUTED = "#5A5A6E"
JAHN_RED_DIM= "#7A0A1A"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {JAHN_DARK};
    color: {JAHN_TEXT};
}}

/* Top accent bar */
[data-testid="stAppViewContainer"] > .main::before {{
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, {JAHN_RED} 0%, #FF4060 50%, {JAHN_RED} 100%);
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
}}

.main {{ background-color: {JAHN_DARK}; padding-top: 4px; }}
.block-container {{ padding-top: 1.5rem; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {JAHN_CARD};
    border-right: 1px solid {JAHN_BORDER};
}}
[data-testid="stSidebar"] label {{
    color: {JAHN_MUTED} !important;
    font-size: 10px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {{
    color: {JAHN_MUTED} !important;
}}

/* Slider accent */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {{
    background: {JAHN_RED} !important;
}}
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {{
    background: {JAHN_RED} !important;
}}

/* Buttons */
.stButton button {{
    background: {JAHN_RED} !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}
.stDownloadButton button {{
    background: {JAHN_RED} !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {{
    color: {JAHN_MUTED} !important;
    border-bottom: 2px solid transparent;
    font-size: 13px;
    font-weight: 500;
}}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    color: {JAHN_RED} !important;
    border-bottom: 2px solid {JAHN_RED} !important;
}}

/* Metric cards */
.jahn-card {{
    background: {JAHN_CARD};
    border: 1px solid {JAHN_BORDER};
    border-top: 2px solid {JAHN_RED};
    border-radius: 8px;
    padding: 14px 16px;
    text-align: center;
    margin-bottom: 4px;
}}
.jahn-card .val {{
    font-family: 'DM Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    color: {JAHN_TEXT};
    line-height: 1.2;
}}
.jahn-card .lbl {{
    font-size: 10px;
    color: {JAHN_MUTED};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}}

/* Section divider */
.section-div {{
    height: 1px;
    background: linear-gradient(90deg, {JAHN_RED}44 0%, {JAHN_BORDER} 100%);
    margin: 12px 0;
}}
.section-title {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: {JAHN_RED};
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid {JAHN_BORDER};
}}

/* Dataframe */
[data-testid="stDataFrame"] {{
    border: 1px solid {JAHN_BORDER};
    border-radius: 8px;
    overflow: hidden;
}}

/* Multiselect tags */
[data-baseweb="tag"] {{
    background-color: {JAHN_RED_DIM} !important;
    color: white !important;
}}

/* Checkboxes */
[data-testid="stCheckbox"] label span {{
    color: {JAHN_TEXT} !important;
}}

/* Success/warning */
.stSuccess {{ background: #0A2A0A !important; border-color: #1B5E20 !important; }}
.stWarning {{ background: #2A1A00 !important; border-color: #F57F17 !important; }}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("data/scouting_app_data.csv")

B = {
    'psv_med': 29.45, 'psv_q75': 30.04,
    'hsr_bip': 789.6, 'spr_bip': 285.6, 'hi_bip': 1086.3, 'expl_bip': 1.32,
    'hsr_otip': 386.9, 'spr_otip': 118.5, 'hi_otip': 500.9, 'expl_otip': 0.45,
    't_hsr': 0.66, 't_sprint': 1.315,
}

TIER_COLORS = {
    '🔥 ELITE TARGET': '#C8102E',
    '🟢 TOP TARGET':   '#1B5E20',
    '🔵 INTERESTING':  '#0D47A1',
    '🟡 WATCHLIST':    '#F57F17',
    '🔴 RISIKO':       '#4A0D0D',
}
TIER_BG = {
    '🔥 ELITE TARGET': '#3D0008',
    '🟢 TOP TARGET':   '#0A1F0A',
    '🔵 INTERESTING':  '#060E1F',
    '🟡 WATCHLIST':    '#1F1200',
    '🔴 RISIKO':       '#1A0404',
}
SPEED_COLORS = {
    '⚡ ELITE':  '#C8102E', '🔵 HIGH': '#1565C0',
    '🟡 FAST':  '#0288D1', '🟠 MEDIUM': '#EF6C00', '—': '#2A2A35',
}

def recalc_ifi(df, w_rq, w_dr, w_bt):
    df = df.copy()
    total_w = w_rq + w_dr + w_bt
    if total_w == 0:
        df['IFI Index'] = 0.0
        df['IFI Punkte'] = 0
    else:
        df['IFI Index'] = (
            df['Run Quality'].fillna(0) * (w_rq / total_w) +
            df['Dribbling'].fillna(0)   * (w_dr / total_w) +
            df['Box Threat'].fillna(0)  * (w_bt / total_w)
        ).round(3)
        df['IFI Punkte'] = df['IFI Index'].apply(
            lambda ts: 5 if ts>=2.0 else (4 if ts>=1.5 else (3 if ts>=0.5 else
                       (2 if ts>=0.0 else (1 if ts>=-0.5 else 0))))
        )
    df['Final Total'] = df['Physical Score'] + df['IFI Punkte']

    def _tier(row):
        total = row['Final Total']
        ifi   = row['IFI Punkte']
        if ifi < 2:
            return '🟡 WATCHLIST' if total >= 10 else '🔴 RISIKO'
        if total >= 20: return '🔥 ELITE TARGET'
        if total >= 17: return '🟢 TOP TARGET'
        if total >= 14: return '🔵 INTERESTING'
        if total >= 10: return '🟡 WATCHLIST'
        return '🔴 RISIKO'

    df['Final Tier'] = df.apply(_tier, axis=1)
    return df

df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + Club name
    st.markdown(f"""
    <div style="text-align:center; padding: 16px 0 8px 0;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="width:90px; filter: drop-shadow(0 2px 8px #C8102E66);">
        <div style="font-family:'DM Sans',sans-serif; font-size:13px;
                    font-weight:700; color:#F0F0F0; margin-top:8px;
                    letter-spacing:0.05em;">JAHN REGENSBURG</div>
        <div style="font-size:10px; color:#5A5A6E; letter-spacing:0.15em;
                    text-transform:uppercase; margin-top:2px;">Scouting · Wide Attacker</div>
    </div>
    <div style="height:1px; background:linear-gradient(90deg,#C8102E44,#1E1E24); margin:8px 0 16px 0;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Filter</div>', unsafe_allow_html=True)

    ligen = sorted(df_raw['Liga'].unique().tolist())
    sel_ligen = st.multiselect("Liga", ligen, default=ligen)

    psv_min = st.slider("PSV-99 Minimum (km/h)", 27.0, 32.5, 29.45, 0.1, format="%.2f")

    alter_range = st.slider("Alter",
        int(df_raw['Alter'].min()), int(df_raw['Alter'].max()),
        (int(df_raw['Alter'].min()), int(df_raw['Alter'].max())))

    min_range = st.slider("Minuten gespielt",
        int(df_raw['Minuten'].min()), int(df_raw['Minuten'].max()),
        (200, int(df_raw['Minuten'].max())), step=50)

    all_tiers = ['🔥 ELITE TARGET','🟢 TOP TARGET','🔵 INTERESTING','🟡 WATCHLIST','🔴 RISIKO']
    sel_tiers = st.multiselect("Final Tier", all_tiers, default=all_tiers)

    otip_gate = st.checkbox("Nur OTIP Pass ✅ YES", value=False)

    all_typen = sorted(df_raw['Spielertyp'].unique().tolist())
    sel_typen = st.multiselect("Spielertyp", all_typen, default=all_typen)

    st.markdown('<div class="section-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 IFI Gewichtung</div>', unsafe_allow_html=True)

    w_rq = st.slider("Run Quality", 0, 100, 25, 5, format="%d%%")
    w_dr = st.slider("Dribbling",   0, 100, 50, 5, format="%d%%")
    w_bt = st.slider("Box Threat",  0, 100, 25, 5, format="%d%%")
    total_w = w_rq + w_dr + w_bt
    if total_w != 100:
        st.warning(f"Summe: {total_w}% (sollte 100% sein)")
    else:
        st.success("Summe: 100% ✓")

    st.markdown('<div class="section-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sortierung</div>', unsafe_allow_html=True)
    sort_col = st.selectbox("Sortieren nach", [
        "Final Total", "Physical Score", "PSV-99", "IFI Index",
        "OTIP Score", "BIP Score", "Burst Score", "Alter", "Minuten"
    ])

# ── FILTER & RECALC ───────────────────────────────────────────────────────────
df = recalc_ifi(df_raw, w_rq, w_dr, w_bt)
mask = (
    df['Liga'].isin(sel_ligen) &
    (df['PSV-99'] >= psv_min) &
    (df['Alter'] >= alter_range[0]) & (df['Alter'] <= alter_range[1]) &
    (df['Minuten'] >= min_range[0]) & (df['Minuten'] <= min_range[1]) &
    df['Final Tier'].isin(sel_tiers) &
    df['Spielertyp'].isin(sel_typen)
)
if otip_gate:
    mask = mask & (df['OTIP Pass'] == '✅ YES')

df_f = df[mask].sort_values(sort_col, ascending=False).reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown(f"""
    <img src="data:image/png;base64,{LOGO_B64}"
         style="width:56px; margin-top:4px; filter:drop-shadow(0 2px 6px #C8102E55);">
    """, unsafe_allow_html=True)
with col_title:
    st.markdown(f"""
    <div style="padding-top:4px;">
        <span style="font-size:22px; font-weight:700; color:#F0F0F0;">Wide Attacker Scouting</span>
        <span style="font-size:13px; color:#5A5A6E; margin-left:12px;">
            Jahn Regensburg · 7 Ligen · {len(df_f)} Spieler nach Filter
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-div" style="margin:8px 0 16px 0;"></div>', unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
cols = st.columns(6)
kpis = [
    (len(df_f),                                                          "Spieler gesamt"),
    (len(df_f[df_f['Final Tier'].isin(['🔥 ELITE TARGET','🟢 TOP TARGET'])]), "Elite + Top"),
    (len(df_f[df_f['OTIP Pass']=='✅ YES']),                             "OTIP Pass ✅"),
    (f"{df_f['PSV-99'].max():.2f}" if len(df_f) else "—",               "Höchste PSV-99"),
    (f"{df_f['Final Total'].max():.1f}" if len(df_f) else "—",          "Bester Score"),
    (f"{int(df_f['Alter'].median())}" if len(df_f) else "—",            "Median Alter"),
]
for col, (val, lbl) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="jahn-card">
            <div class="val">{val}</div>
            <div class="lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Spieler-Liste", "📊 Scatter-Plot", "📖 Scoring Info"])

with tab1:
    st.markdown(f"<div style='font-size:11px;color:#5A5A6E;margin-bottom:8px;font-family:DM Mono,monospace;letter-spacing:0.08em;text-transform:uppercase;'>{len(df_f)} Spieler · Sortiert nach {sort_col}</div>",
                unsafe_allow_html=True)
    if df_f.empty:
        st.info("Keine Spieler mit diesen Filtern.")
    else:
        disp = df_f[[
            'Spieler','Verein','Liga','Alter','Minuten',
            'Final Total','Final Tier','Physical Score',
            'IFI Punkte','IFI Index',
            'Speed Flag','PSV-99','Δ PSV-99','Speed Score',
            'OTIP Pass','OTIP Score','Δ HSR OTIP',
            'BIP Level','BIP Score','Δ HSR BIP',
            'Burst Score','Δ T→HSR',
            'Spielertyp','Run Quality','Dribbling','Box Threat',
            'Transferwert (€)',
        ]].copy()

        def tier_color(val):
            styles = {
                '🔥 ELITE TARGET': 'background-color:#3D0008;color:#FF8099',
                '🟢 TOP TARGET':   'background-color:#0A1F0A;color:#81C784',
                '🔵 INTERESTING':  'background-color:#060E1F;color:#90CAF9',
                '🟡 WATCHLIST':    'background-color:#1F1200;color:#FFE082',
                '🔴 RISIKO':       'background-color:#1A0404;color:#EF9A9A',
            }
            return styles.get(val, '')

        def psv_color(val):
            if pd.isna(val): return ''
            if val >= 32:    return 'background-color:#3D0008;color:#FF8099;font-weight:600'
            if val >= 31:    return 'background-color:#0D2050;color:#90CAF9;font-weight:600'
            if val >= 30.5:  return 'background-color:#003344;color:#80DEEA;font-weight:600'
            if val >= 29.45: return 'background-color:#1F1200;color:#FFCC80;font-weight:600'
            return 'color:#5A5A6E'

        def pos_delta(val):
            if pd.isna(val): return ''
            return 'color:#81C784' if val > 0 else ('color:#EF9A9A' if val < 0 else '')

        def neg_delta(val):
            if pd.isna(val): return ''
            return 'color:#81C784' if val < 0 else ('color:#EF9A9A' if val > 0 else '')

        styled = (disp.style
            .map(tier_color, subset=['Final Tier'])
            .map(psv_color,  subset=['PSV-99'])
            .map(pos_delta,  subset=['Δ PSV-99','Δ HSR OTIP','Δ HSR BIP'])
            .map(neg_delta,  subset=['Δ T→HSR'])
            .format({
                'PSV-99':       '{:.2f}',
                'Final Total':  '{:.1f}',
                'Physical Score': '{:.1f}',
                'IFI Index':    '{:.3f}',
                'Run Quality':  '{:.3f}',
                'Dribbling':    '{:.3f}',
                'Box Threat':   '{:.3f}',
                'Δ PSV-99':     '{:+.2f}',
                'Δ HSR OTIP':   '{:+.0f}',
                'Δ HSR BIP':    '{:+.0f}',
                'Δ T→HSR':      '{:+.3f}',
                'Transferwert (€)': lambda v: f"€{int(v):,}" if pd.notna(v) else '—',
            }, na_rep='—')
            .set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#111115'),
                          ('color', '#5A5A6E'),
                          ('font-size', '11px'),
                          ('text-transform', 'uppercase'),
                          ('letter-spacing', '0.05em'),
                          ('border-bottom', '1px solid #1E1E24')]
            }])
        )

        st.dataframe(styled, use_container_width=True, height=520)

        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Export CSV", csv, "jahn_scouting_export.csv",
                           "text/csv", use_container_width=False)

with tab2:
    st.markdown("<div style='font-size:11px;color:#5A5A6E;margin-bottom:12px;font-family:DM Mono,monospace;letter-spacing:0.08em;text-transform:uppercase;'>Scatter-Plot</div>",
                unsafe_allow_html=True)

    numeric_cols = [
        'PSV-99','Final Total','Physical Score','IFI Index',
        'OTIP Score','BIP Score','Burst Score','Speed Score',
        'Run Quality','Dribbling','Box Threat',
        'HSR OTIP P30','HSR P60BIP','Time→HSR (s)','Alter','Minuten',
        'Δ PSV-99','Δ HSR OTIP','Δ HSR BIP',
    ]

    c1,c2,c3,c4 = st.columns(4)
    with c1: x_axis   = st.selectbox("X-Achse",   numeric_cols, index=0)
    with c2: y_axis   = st.selectbox("Y-Achse",   numeric_cols, index=2)
    with c3: size_col = st.selectbox("Punktgröße",['—'] + numeric_cols, index=0)
    with c4: color_by = st.selectbox("Farbe",     ['Final Tier','Speed Flag','Spielertyp','Liga'], index=0)

    if df_f.empty:
        st.info("Keine Daten für Plot.")
    else:
        try:
            import plotly.express as px

            plot_df = df_f.dropna(subset=[x_axis, y_axis]).copy()
            color_map = TIER_COLORS if color_by == 'Final Tier' else (
                        SPEED_COLORS if color_by == 'Speed Flag' else None)

            size_vals = None
            if size_col != '—' and size_col in plot_df.columns:
                s = pd.to_numeric(plot_df[size_col], errors='coerce').fillna(0)
                s_min, s_max = s.min(), s.max()
                size_vals = (((s-s_min)/(s_max-s_min+0.001))*20+6).tolist()

            fig = px.scatter(
                plot_df, x=x_axis, y=y_axis,
                color=color_by, color_discrete_map=color_map,
                hover_name='Spieler',
                hover_data={'Verein':True,'Liga':True,'Alter':True,
                            'Final Total':':.1f','PSV-99':':.2f',
                            'OTIP Pass':True,'Speed Flag':True, color_by:False},
                size=size_vals, size_max=24,
                template='plotly_dark', height=520,
            )

            if x_axis == 'PSV-99':
                fig.add_vline(x=B['psv_med'], line_dash="dash",
                              line_color="#C8102E66",
                              annotation_text="3.Liga Median",
                              annotation_font_size=10,
                              annotation_font_color="#C8102E")
            if y_axis == 'PSV-99':
                fig.add_hline(y=B['psv_med'], line_dash="dash",
                              line_color="#C8102E66")

            fig.update_layout(
                paper_bgcolor='#0A0A0D', plot_bgcolor='#111115',
                font_family='DM Sans', font_color='#8A8F9E',
                xaxis=dict(gridcolor='#1E1E24', zeroline=False),
                yaxis=dict(gridcolor='#1E1E24', zeroline=False),
                legend=dict(bgcolor='#111115', bordercolor='#1E1E24', borderwidth=1),
                margin=dict(l=40,r=20,t=40,b=40),
            )
            fig.update_traces(marker=dict(line=dict(width=0.5, color='#0A0A0D')))

            st.plotly_chart(fig, use_container_width=True)

        except ImportError:
            st.warning("Plotly nicht installiert.")

with tab3:
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("### Final Total /25")
        st.markdown("""
| Komponente | Faktor | Max |
|---|---|---|
| ⚡ Speed Score (0–4) | ×2.0 | 8 |
| 🏃 OTIP Score (0–4) | ×1.5 | 6 |
| 💥 BIP Score (0–4) | ×1.0 | 4 |
| 🚀 Burst Score (0–4) | ×0.5 | 2 |
| 🎯 IFI Punkte (0–5) | +add | 5 |
| **Total** | | **25** |

**IFI Gate:** IFI Punkte < 2 → max. 🟡 WATCHLIST
        """)
    with c_b:
        st.markdown("### Final Tier")
        st.markdown("""
| Score | Tier |
|---|---|
| ≥ 20 + IFI ≥2 | 🔥 ELITE TARGET |
| ≥ 17 + IFI ≥2 | 🟢 TOP TARGET |
| ≥ 14 + IFI ≥2 | 🔵 INTERESTING |
| ≥ 10 | 🟡 WATCHLIST |
| < 10 | 🔴 RISIKO |

**Speed Flag**
- ⚡ ELITE ≥32.0 km/h
- 🔵 HIGH ≥31.0 km/h
- 🟡 FAST ≥30.5 km/h
- 🟠 MEDIUM ≥29.45 km/h
- — unter Median
        """)
    st.markdown("---")
    st.markdown("### 3.Liga Benchmark (Wide Attacker, ≥500 min, Saison 2024/25)")
    bench_df = pd.DataFrame([
        {"Metrik":"PSV-99 Median","Wert":"29.45 km/h","Layer":"Speed"},
        {"Metrik":"HSR Distance P60BIP","Wert":"789.6m","Layer":"BIP"},
        {"Metrik":"Sprint Distance P60BIP","Wert":"285.6m","Layer":"BIP"},
        {"Metrik":"HI Distance P60BIP","Wert":"1086.3m","Layer":"BIP"},
        {"Metrik":"HSR Distance OTIP P30","Wert":"386.9m","Layer":"OTIP"},
        {"Metrik":"Sprint Distance OTIP P30","Wert":"118.5m","Layer":"OTIP"},
        {"Metrik":"HI Distance OTIP P30","Wert":"500.9m","Layer":"OTIP"},
        {"Metrik":"Time to HSR","Wert":"0.66s","Layer":"Burst"},
        {"Metrik":"Time to Sprint","Wert":"1.315s","Layer":"Burst"},
    ])
    st.dataframe(bench_df, use_container_width=True, hide_index=True)
