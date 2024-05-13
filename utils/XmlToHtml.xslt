<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" doctype-system="about:legacy-compat" encoding="UTF-8" indent="yes"/>
  
  <!-- Template for the HTML structure -->
  <xsl:template match="/">
    
    <html lang="it">
      <head>
        <title>Ricevuta di Riparazione Telefonica</title>
        <style>
          *{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          }
          
          .receipt{
          box-shadow: 6px 6px 10px rgba(95, 95, 95, 0.437);
          width: 45%;
          margin: auto;
          }
          
          .receipt-head{
          display:flex;
          align-items: flex-start;
          gap:400px;
          border-bottom: 2px solid black;
          padding: 15px;
          margin: 10px;
          }
          
          .company-details{
          text-align: right;
          }
          
          .client-details{
          padding: 10px;
          width: 40%
          }
          
          .client-details p{
          margin: 5px;
          font-weight:500;
          color: #3f3f3f;
          }
          
          .repair-info{
          margin-top: 50px;
          }
          
          table{
          width: 100%;
          padding: 10px;
          text-align: center;
          }
          .table-head{
          background-color: rgb(207, 215, 233);
          padding: 15px;
          }
          
          .table-data{
          background-color: rgb(246, 246, 246);
          padding: 10px;
          border: 1px solid #303030;
          }
          
          .terms-conditions{
          width: 60%;
          margin: 40px auto;
          text-align: center;
          
          }
          
          .banner{
          text-align: center;
          padding: 10px;
          }
          
          .banner img{
          width: fit-content;
          width: 50%;
          }
        </style>
      </head>
      <body>
        <!-- full receipt details -->
        <div class="receipt">
          <!-- company details -->
          <div class="receipt-head">
            <div class="receipt-header">
              <img src="img/logo.webp" alt="spazioexe logo"/>
            </div>
            <div class="company-details">
              <strong>Scheda : #RP20240503-1</strong><br/>
              Spazio Ex&#233; s.r.l.<br/>
              via Roma 7<br/>
              San Vito al Tagliamento, 33078 PN <br/>
              Tel: 00334686090978
            </div>
          </div>
          
          <!-- client details -->
          <div class="client-details">
            <h3>DETTAGLI CLIENTE</h3>
            <xsl:value-of select="/items/item/first_name"/>&#160;<xsl:value-of select="/items/item/last_name"/><br/>
            <xsl:value-of select="/items/item/request_date"/><br/>
            <xsl:value-of select="/items/item/device"/><br/>         
            <xsl:value-of select="/items/item/brand"/><br/>
            <xsl:value-of select="/items/item/model"/><br/>
            <xsl:value-of select="/items/item/left_accessory"/><br/>
            <xsl:value-of select="/items/item/device"/><br/>
            Tel:<xsl:value-of select="/items/item/phone_number"/>
          </div>
          
          <!-- description of service given -->
          <div class="repair-info">
            <table>
              <tr>
                <th class="table-head">Descrizione</th>
                <th  class="table-head">Costo</th>
              </tr>
              <xsl:for-each select="/items/item/action">
                <tr>
                  <td><xsl:value-of select="."/>&#160; : <xsl:value-of select="../details"/></td>
                  <td>€&#160;<xsl:value-of select="../price"/></td>
                </tr>
              </xsl:for-each>
            </table>
          </div>
          
          
          <!-- terms and conditions -->
          <div class="terms-conditions">
            <h4>Termini e Condizioni</h4>
            <div class="term">
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse quam orci, mollis nec iaculis ac, euismod sed eros. Etiam iaculis lectus elit, sed placerat orci facilisis suscipit. Aliquam quis arcu turpis. In viverra ultricies nibh eget rhoncus. Duis ut magna ac mi eleifend posuere. Sed fringilla semper lectus in bibendum. Sed dapibus felis nulla, ut venenatis tellus vestibulum eget. Proin leo lorem, venenatis at interdum sed, posuere posuere tellus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nulla sollicitudin enim eu orci feugiat luctus. Cras at diam nec eros tempus tempor vel eget eros. Pellentesque sed justo vel ipsum vestibulum varius at at nulla. Mauris blandit neque magna, et consectetur justo porta et. Quisque ultrices, leo at semper scelerisque, tellus nisl mollis ex, et interdum sem ligula vel leo.
                Fusce augue sapien, dictum et metus sit amet, interdum volutpat augue. Sed id volutpat nunc. Cras a hendrerit lectus, sed egestas lectus. Integer vel lorem maximus, gravida sapien eu, rutrum neque. Aenean vitae dapibus dui. Praesent elementum felis ante, a faucibus justo condimentum nec. Cras in mi quam. Etiam vehicula lorem quis eros rutrum dignissim. Aliquam condimentum mollis urna eu congue. Sed quis sollicitudin dui, vel gravida odio. Sed varius urna nisi, at ullamcorper purus pretium nec. Cras nec tellus mauris. 
              </p>           
            </div>
          </div>
          
          <!-- banner spot -->
          <div class="banner">
            <img src="images/banner.png" alt="banner spazio exe"/>
          </div>
        </div>
      </body>
    </html>
    
  </xsl:template>
</xsl:stylesheet>
