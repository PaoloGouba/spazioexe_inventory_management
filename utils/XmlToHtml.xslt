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
              Spazio Exe<br/>
              P.IVA/C.F. BNDMNR98S22Z354H<br/>
              VIA POMPONIO AMALTEO 16<br/>
              San Vito al Tagliamento, 33078 PN <br/>
              Tel: 00334686090978 <br/>
              info@spazioexe.com<br/>
              + (39)376 175 1181
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
              <xsl:for-each select="/items/item">
                
                <xsl:choose>
                  <!-- Condizione se acconto è maggiore di zero -->
                  <xsl:when test="acconto > 0">
                    <tr>
                      <td>ciao<xsl:value-of select="."/>&#160; : <xsl:value-of select="details"/></td>
                      <td>€&#160;<xsl:value-of select="price - acconto"/></td>
                    </tr>
                    <tr>
                      <td>Acconto</td>
                      <td>€&#160;<xsl:value-of select="acconto"/></td>
                    </tr>
                  </xsl:when>
                  <!-- Condizione se acconto è uguale a zero o vuoto -->
                  <xsl:otherwise>
                    <tr>
                      <td>ciao<xsl:value-of select="."/>&#160; : <xsl:value-of select="details"/></td>
                      <td>€&#160;<xsl:value-of select="price"/></td>
                    </tr>
                  </xsl:otherwise>
                </xsl:choose>
                
              </xsl:for-each>
            </table>
          </div>
          
          
          <!-- terms and conditions -->
          <div class="terms-conditions">
            <h4>Termini e Condizioni</h4>
            <div class="term">
              <p>
                Prima di consegnare il tuo dispositivo in riparazione, effettua il backup di tutte le informazioni e dei dati salvati sul dispositivo per evitare la perdita o il danneggiamento durante il processo di test o ispezioni. Purtroppo Spazio Exe non è responsabile in nessuna circostanza, sia espressamente che implicitamente, per eventuali danni di qualsiasi tipo causati da perdita, danneggiamento o corruzione del contenuto dei dati durante la riparazione o la sostituzione del prodotto. Se il cliente smarrisce la copia cliente del modulo, potrà ritirare il prodotto con un valido documento di riconoscimento.<br/>
                N.B. In alcuni casi, la riparazione del prodotto può comportare la perdita dei dati in esso contenuti: è ad esclusivo carico del cliente il salvataggio degli stessi prima dell'invio in riparazione. Punto Elettronico non si ritiene in alcun modo responsabile dei dati contenuti nel prodotto.<br/>
                Il cliente è tenuto al ritiro del prodotto entro tre mesi (novanta giorni) dalla data di comunicazione di avvenuta riparazione, decorso tale termine Spazio Exe si riterrà libero di poter smaltire il prodotto a norma di legge in quanto non ritirato entro i termini indicati.<br/>
                Il cliente accetta implicitamente le condizioni al momento della presa in carico dell'ordine.
                
              </p>           
            </div>
          </div>
          
          <!-- banner spot -->
          <div class="banner">
            <img src="img/new_banner.jpg" alt="banner spazio exe"/>
          </div>
        </div>
      </body>
    </html>
    
  </xsl:template>
</xsl:stylesheet>
