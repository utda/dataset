# 東京大学学術資産等アーカイブズ共用サーバ - データセット

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)  

[東京大学学術資産等アーカイブズ共用サーバ](https://iiif.dl.itc.u-tokyo.ac.jp/repo/)（以下、共用サーバ）で公開するコレクションのデータセットを公開します。
各データセットは以下の要素から構成されます。

<dl>
<dt>画像</dt>
<dd>
画像に関する情報をIIIFコレクション（IIIFマニフェストのリスト）形式で提供します。
</dd>
<dt>メタデータ</dt>
<dd>
コレクション中のアイテムのメタデータの一覧をCSV, MS-Excel, JSON-LD形式で提供します。
</dd>
<dt>テキスト</dt>
<dd>
一部のコレクションでは、テキストデータを公開しています。RTF形式とTEI/XML形式で提供します。
</dd>
</dl>

* IIIF: [International Image Interoperability Framework](https://iiif.io/)
* TEI: [Text Encoding Initiative](http://www.tei-c.org/)  

***

ディレクトリ構造は以下の通りです。

```
docs/collections
│
└───collection A
|   │
|   └───image
|   │   │   collection.json
|   │
|   └───metadata
|   │   │   data.json
|   │   │   data.xlsx
|   │   │   data.csv   
|   │
|   └───text
|       └───rtf   
|       │   |   xxx.rtf
|       │   |   yyy.rtf       
|       │   |   ...
|       │
|       └───xml
|       │   |   xxx.xml
|       │   |   yyy.xml       
|       │   |   ...        
|
└───collection B
|   |   ...
```