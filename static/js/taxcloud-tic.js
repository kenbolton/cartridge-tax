//currentTic must be declared/set, even if TIC has not already been specified.
var currentTic = "";

//the ID of the HTML form field to be replaced
var fieldID = "id_tic";

//UI options
//set the the dropdownlist match your page/form CSS
var dropdownListCss = "font-size:small;background-color:#yellow;border:solid 1px #BBBBFF;font-family:'Trebuchet MS', Arial, Helvetica, sans-serif;";

//CSS to be used by the drop-down-menu list
var resultsListCss = "font-size:small;color:#666666;font-family:'Trebuchet MS';text-decoration:none;cursor:default;"

//CSS to be used to display TIC selection path
var linkClass = "navlink"; //CSS Class to by used for links - not used if usImageButtons set to true

//Use image buttons instead of links for submit and reset/start-over features
//Default = true
var useImageButtons = true; 

//Do you want to show the "Start Over" link once selection has been made - just in case...
//Default = true
var showStartOverLink = true; 


(function () {
  var tcJsHost = (("https:" == document.location.protocol) ? "https:" : "http:");
  var ts = document.createElement('script');
  ts.type = 'text/javascript';
  ts.async = true;
  ts.src = tcJsHost + '//taxcloud.net/jquery.tic2.public.js';
  var t = document.getElementsByTagName('script')[0];
  t.parentNode.insertBefore(ts, t);
})();
