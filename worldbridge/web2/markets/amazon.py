---
<(META)>:
  DOCid:
  name: <[document_name]>
  description: >
  version: <[version]>
  path: <[LEXIvrs]><[path]>.yaml
  outline: <[outline]>
  authority: <[authority]>
  security: <[seclvl]>
  <(WT)>: -32

<[SKRP:.hrid]>:
  name: xstat
  text: >
    xstat() {
      for target in "${@}"; do
        inode=$(ls -di "${target}" | cut -d ' ' -f 1)
        fs=$(df "${target}"  | tail -1 | awk '{print $1}')
        crtime=$(sudo debugfs -R 'stat <'"${inode}"'>' "${fs}" 2>/dev/null |
        grep -oP 'crtime.*--\s*\K.*')
        printf "%s\t%s\n" "${crtime}" "${target}"
      done
    }
  processor: bash

MTF0000.0000.0000:
  Name: &IDCT Item Data Consolidation Template
  Description: >
  IDs:
    - uuid:
    - name: *IDCT
  Methods:
    LEXI:
      Type:
      Loci: #data container for any pictures, models, test data, etc this is some combo of datavein and thingery
      Size:
        Weight:
        Envelope:
        Rate:
        Expire:
        Deteriation: #rate at which something gets worse or better in rare cases...impacts to the value
      Summary:
      Extended:
        <@[source]@>:
          details:
            <[xpath]>/template
          raw:
      PullFrom: #any already procured source within the concern
      Purchase:
        - <@[source]@>
      Manufacture:
        - <@[source]@> #handle internal mfg and contract mfg operations
      Reclaim:
        - <@[source]@> #need to handle many processes but only to the level of refurbishment
        #true recycling back to a raw material doesn't qualify that would become
        #a manufacturing process
        #An Item is Transferable
        #An Item is a Product, or a Service
        #An Item has a Description
        #An Item has at least 1 Review -> A Review comes from Proud Peacock
        #An Item has a Sales Analysis -> A Sales Analysis comes from Maliable Moose
        #A Sales Price has a Discount -> A Discount comes from Dazzling Dungbeetle
MTF0000.0000.0000:
  Name: &IDET Information Data Extraction Template
  Description: >
  IDs:
    - uuid:
    - name: *IDET
  Methods:
    Amazon:
      format: xml
      fields:
        NAME: URBEST Inlet Module Plug 5A Fuse Switch Male Power Socket 10A 250V 3 Pin IEC320 C14
        SALE_PRICE: $6.99
        CATEGORY: Industrial & Scientific > Industrial Electrical > Wiring & Connecting > IC Sockets & Plugs
        ORIGINAL_PRICE: $6.99
        AVAILABILITY: In Stock.
        URL: https://www.amazon.com/gp/product/B00ME5YAPK/ref=ppx_yo_dt_b_asin_title_o02__o00_s01?ie=UTF8&psc=1
        Product Name : Power Socket w Switch Fuse;
        Material (External) : Plastic, Metal;
        Color : Red, Silver Tone, Silver Tone
        Voltage & Current : 10A, 250V AC;
        Hole in Top Face Diameter : 0.42cm / 0.16"
        Hole Center Distance : 3.9cm / 1.5";
        Bottom Size : 4.7 x 2.7cm / 1.9" x 1.1"(L*W)
        Total Size : 5.8 x 4.8 x 3.4cm / 2.3" x 1.9" x 1.3"(L*W*H);
        Plug Type : 3 Pin IEC320 C14
        Weight : 24g;
        Package Content : 1 x Power Socket
    eBay:
      format: html

    Google:
      Description: >
        Extraction information from Search results...advert results...shopping prices?
      format: html

    Wikipedia:
      format: html
