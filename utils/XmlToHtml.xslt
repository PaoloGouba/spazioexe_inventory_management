<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" doctype-system="about:legacy-compat" encoding="UTF-8" indent="yes"/>

  <!-- Template for the HTML structure -->
  <xsl:template match="/">
    <html lang="it">
      <head>
        <meta charset="UTF-8"/>
        <title>Ricevuta di Riparazione Telefonica</title>
        <style>
          body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            color: black;
            font-size: 12px;
          }
          .receipt-container {
            width: 210mm;
            min-height: 297mm;
            padding: 10mm;
            box-sizing: border-box;
            page-break-after: always;
          }
          header {
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
            margin-bottom: 10px;
          }
          .logo {
            width: 100px;
            float: left;
          }
          .logo img {
            width: 35%;
            height: auto;
          }
          .company-details {
            float: right;
            text-align: right;
            line-height: 1.5;
          }
          .clear-fix {
            clear: both;
          }
          .customer-details, .repair-details, .total-cost {
            width: 100%;
            margin-bottom: 15px;
          }
          th, td {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid #ddd;
          }
          th {
            background-color: #f2f2f2;
          }
          .total-cost {
            text-align: right;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
          }
        </style>
      </head>
      <body>
        <div class="receipt-container">
          <header>
            <div class="logo">
              <img src="img/logo.webp" alt="Logo Azienda"/>
            </div>
            <div class="company-details">
              <strong>Scheda : #RP20240503-1<br/></strong>
              Spazio Exé s.r.l.<br/>
              via Roma N 7<br/>
              San Vito al Tagliamento, 33078 PN <br/>
              Tel: 00334686090978
            </div>
            <div class="clear-fix"></div>
          </header>
          <div class="customer-details">
            <strong>Dettagli Cliente:</strong><br/>
            <xsl:value-of select="/items/item/first_name"/>&#160;<xsl:value-of select="/items/item/last_name"/> <br/>
            <xsl:value-of select="/items/item/request_date"/><br/>
            <xsl:value-of select="/items/item/device"/><br/>           
             <xsl:value-of select="/items/item/brand"/><br/>
            <xsl:value-of select="/items/item/model"/><br/>
            <xsl:value-of select="/items/item/left_accessory"/><br/>

            <xsl:value-of select="/items/item/device"/><br/>

            Tel:<xsl:value-of select="/items/item/phone_number"/>
          </div>
          <div class="repair-details">
            <strong>Dettagli della Riparazione:</strong><br/>
            <table>
              <tr><th>Descrizione</th><th>Costo</th></tr>
              <xsl:for-each select="/items/item/action">
                <tr>
                  <td><xsl:value-of select="."/>&#160; : <xsl:value-of select="../details"/></td>
                  <td>€&#160;<xsl:value-of select="../price"/></td>
                </tr>
              </xsl:for-each>
            </table>
          </div>
          <!-- <div class="total-cost"> 
            Costo Totale: €<xsl:value-of select="/customer/product/price"/>
          </div> -->
        </div>
        <p>
         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse quam orci, mollis nec iaculis ac, euismod sed eros. Etiam iaculis lectus elit, sed placerat orci facilisis suscipit. Aliquam quis arcu turpis. In viverra ultricies nibh eget rhoncus. Duis ut magna ac mi eleifend posuere. Sed fringilla semper lectus in bibendum. Sed dapibus felis nulla, ut venenatis tellus vestibulum eget. Proin leo lorem, venenatis at interdum sed, posuere posuere tellus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nulla sollicitudin enim eu orci feugiat luctus. Cras at diam nec eros tempus tempor vel eget eros. Pellentesque sed justo vel ipsum vestibulum varius at at nulla. Mauris blandit neque magna, et consectetur justo porta et. Quisque ultrices, leo at semper scelerisque, tellus nisl mollis ex, et interdum sem ligula vel leo.
         Fusce augue sapien, dictum et metus sit amet, interdum volutpat augue. Sed id volutpat nunc. Cras a hendrerit lectus, sed egestas lectus. Integer vel lorem maximus, gravida sapien eu, rutrum neque. Aenean vitae dapibus dui. Praesent elementum felis ante, a faucibus justo condimentum nec. Cras in mi quam. Etiam vehicula lorem quis eros rutrum dignissim. Aliquam condimentum mollis urna eu congue. Sed quis sollicitudin dui, vel gravida odio. Sed varius urna nisi, at ullamcorper purus pretium nec. Cras nec tellus mauris. 
        </p>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
