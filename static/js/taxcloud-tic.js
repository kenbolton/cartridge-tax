/*
TaxCloud TIC Display Selector 2.0
This JavaScript will dynamically create a drop down list to allow the select of an up-to-date SSUTA Taxability Classification.
JQuery javascript library must be referenced/included on the page BEFORE reference to this javascript helper.
This JavaScript is provided as a convenience for TaxCloud Merchants pursuant to the Fed-Tax.net Public Source License (https://taxcloud.net/ftpsl.pdf) 
*/

//TaxCloud Specific
var tcJsHost = (("https:" == document.location.protocol) ? "https:" : "http:");
var TaxCloudUrl = tcJsHost + "//taxcloud.net/"; //URL for TaxCloud (default --> https://taxcloud.net/)
var TaxCloudTicUrl = TaxCloudUrl + "tic/"; //URL to the TIC feed (default --> https://taxcloud.net/tic/)
/*
//Merchant Implementation
var currentTic = ""; //currentTic should be declared/set via JavaScript in the calling page if TIC has already been specified.
var fieldID = "taxcloudJqueryTicFlea"; //the ID of the generated form field to by used by Merchant's system to identify and persist the selected TIC
var itemID = ""; //itemID should be declared/set via JavaScript in the calling page to specify Merchants internal identifier for the Item being classified
var itemIDField = ""; //the ID of the generated form field to by used by Merchant's system to identify the Item being classified
//set the UI display of the dropdownlist match your page/form CSS
var dropdownListCss = "font-size:small;background-color:#ECECFF;border:solid 1px #BBBBFF;font-family:'Trebuchet MS', Arial, Helvetica, sans-serif;"; //CSS to be used by the drop-down-menu list
var resultsListCss = "font-size:small;color:#666666;text-decoration:none;cursor:default;"//CSS to be used to display TIC selection path
var linkClass = "navlink"; //CSS Class to by used for links - not used if usImageButtons set to true
var useImageButtons = true; //Use image buttons instead of links for submit and reset/start-over features
var showStartOverLink = true; //Do you want to show the "Start Over" link once selection has been made - just in case...
//if you would like to store/save this category selection inline, set to true
//if the page/form using this control already has a submit button, this should be set to false -- be sure the target of your page/form looks for the "fieldID" identified above to persist the selected TIC
var withSubmit = true;
var submitTarget = ""; //if withSubmit is set to true, what is the URL target to persist the selected TIC
var submitMethod = "GET"; //set to GET or POST based upon the submitTarget's expected method
*/

//currentTic must be declared/set, even if TIC has not already been specified.
var currentTic = $('#id_tic').val();

//the ID of the HTML form field to be replaced
var fieldID = "id_tic";

//UI options
//set the the dropdownlist match your page/form CSS
var dropdownListCss = "font-size:small;";

//CSS to be used by the drop-down-menu list
var resultsListCss = "font-size:small;text-decoration:none;cursor:default;"

//CSS to be used to display TIC selection path
var linkClass = "navlink"; //CSS Class to by used for links - not used if usImageButtons set to true

//Use image buttons instead of links for submit and reset/start-over features
//Default = true
var useImageButtons = false; 

//Do you want to show the "Start Over" link once selection has been made - just in case...
//Default = true
var showStartOverLink = true; 

//DO NOT CHANGE ANYTHING BELOW HERE!
var ct = ((typeof currentTic == 'undefined') ? "" : currentTic);

//Set Defaults if properties not set by the calling page
var ddlcss = ((typeof dropdownListCss == 'undefined') ? "font-size:small;background-color:#ECECFF;border:solid 1px #BBBBFF;font-family:'Trebuchet MS', Arial, Helvetica, sans-serif;" : dropdownListCss);
var rescss = ((typeof resultsListCss == 'undefined') ? "font-size:small;color:#666666;text-decoration:none;cursor:default;" : resultsListCss);
var lc = ((typeof linkClass == 'undefined') ? "navlink" : linkClass);
var ub = ((typeof useImageButtons == 'undefined') ? true : useImageButtons);
var so = ((typeof showStartOverLink == 'undefined') ? true : showStartOverLink);
var ws = ((typeof withSubmit == 'undefined') ? false : withSubmit);
var st = ((typeof submitTarget == 'undefined') ? "" : submitTarget);
var sm = ((typeof submitMethod == 'undefined') ? "GET" : submitMethod);

var ticJSON;

var foundTic = false;
var curSelectedTic = "";
var foundTicObj = false;

var prevTIC = "";
var saveTIC = "";

var catListID = "catList";
var ticFinalID = "jqTicFinal";
var ticCompleteID = "ticComplete";

if ($('#' + catListID).length != 0) {
  var catListID = "catList" + $('#' + catListID).length;
  var ticFinalID = "jqTicFinal" + $('#' + ticFinalID).length;
  var ticCompleteID = "ticComplete" + $('#' + ticCompleteID).length;
}

$(document).ready(function() {
  var reqs = new Array("currentTic", "fieldID", "itemID", "itemIDField");
  if (checkRequirements(reqs)) {
    var jqReplace = "#" + fieldID;
    $(jqReplace).parent().prepend('<span style="' + rescss + '" id="' + catListID + '"></span><span style="' + rescss + '" id="' + ticFinalID + '">[Loading...]</span><span id="' + ticCompleteID + '"></span>')
    $('#catList').html('');
    $('#jqTicFinal').html('<select style="' + ddlcss + '" id="' + fieldID + '" onchange="getTic(this)"><option>[ Loading... ]</option></select>');
    $('#ticComplete').html('');
    jsonp();
    if (ct.length != 0) {
      saveTIC = ct;
    }
  }
});

function checkRequirements(reqs) {
  var x;
  for (x in reqs) {
    var errorString = "undefined";
    var isOK = false;
    try {
      if (typeof eval(reqs[x]) == 'undefined') {
        isOK = false;
      } else if (eval(reqs[x]) == "") {
        errorString = "empty";
        if (reqs[x] == "currentTic") { //currentTic can be empty
          isOK = true;
        }
      } else if (eval(reqs[x]) != "") {
        isOK = true;
      }
    } catch (e) {
      isOK = false;
      if ((!ws) && ((reqs[x] == "itemIDField") || (reqs[x] == "itemID"))) { //if not submitting, we dont need
        isOK = true;
      }
      if ((ws) && ((reqs[x] == "itemIDField") || (reqs[x] == "itemID"))) { //if submitting, we do need
        errorString += " but is required when <i>withSubmit=true</i>";
      }
    }
    if (!isOK) {
      $("body").append("<div style='margin:0px;padding:10px 0px 10px 0px;text-align:center;font-family:verdana;position:relative;top:0px:left:0px;width:" + $("body").width() + ";z-index:100;color:#000000;background:#FFCC00;border:1px solid #000066;'>TaxCloud JS TIC Selector ERROR: javascript <b style='color:#000000;'>" + reqs[x] + "</b> var is <b style='color:#000000;'>" + errorString + "</b>.</div>");
    }
  }
  return isOK;
}

function revert() {
  if (saveTIC.length == 5) {
    ct = saveTIC;
    foundTic = false;
  }
  $('#ticComplete').html("");
  showTic();
}

function showTic() {
  if (ct.length != 5) {
    if ((ct.length != 0) && (ct != "&nbsp;")) {
      alert("The current TIC specified for this item (TIC:" + ct + ") is invalid.\n\nPlease select an appropriate taxability category from the drop down list.");
    }
    $('#catList').html("");
    $('#jqTicFinal').html('<select style="' + ddlcss + '" id="' + fieldID + '" onchange="getTic(this)"><option>[ Loading... ]</option></select>');
    var ticSelector = $("#" + fieldID);
    var ticSelector = $("#" + fieldID);
    if (ticJSON.length > 0) {
      $.each(ticJSON, function(i, item) {
        addOption(ticSelector, item.tic)
      });
    }
    ticSelector.children(":first").text("[ - Select - ]").attr("selected", true);
  } else {
    $('#catList').html("");
    $('#jqTicFinal').html("<input type='hidden' id='" + fieldID + "' value='" + ct + "'/>");
    $('#ticComplete').html("");
    var selectedObj = find(ct, ticJSON);
    $('#catList').prepend(" (TIC:<span title='" + selectedObj.tic.title + ":[Click to edit]' class='" + lc + "' onclick='showTic()' style='cursor:pointer;'>" + selectedObj.tic.id + "</span>)");
    var myTitleString = selectedObj.tic.title;
    if (myTitleString.length > 40) {
      myTitleString = myTitleString.substring(0, 40) + "[...]"
    }
    $('#catList').prepend(myTitleString);
    ct = "";
  }
}

function jsonp() {
  var url = TaxCloudTicUrl + "?format=jsonp"
  url += "&time=";
  url += new Date().getTime().toString(); // prevent caching        
  var script = document.createElement("script");
  script.setAttribute("src", url);
  script.setAttribute("type", "text/javascript");
  document.body.appendChild(script);
}

function addOption(ticSelector, tic) {
  var hasChildren = "";
  if (tic.children) {
    hasChildren = "..."
  }
  if (tic.ssuta == 'true') {
    ticSelector.append('<option value="' + tic.id + '" title="' + tic.title + ' (SSUTA)" style="font-weight:bold !important;">' + tic.label + ' ' + hasChildren + '</option>');
  } else {
    ticSelector.append('<option value="' + tic.id + '" title="' + tic.title + '">' + tic.label + hasChildren + '</option>');
  }
}

function taxcloudTics(ptics) {
  var ticListObj = ptics.tic_list;
  ticJSON = ptics.tic_list;
  showTic();
}

function saveTic() {
  var newTic = $('#' + fieldID).val();
  if (sm.toUpperCase() == "GET") {
    $.get(st, {
      fieldID: newTic,
      itemIDField: itemID
    }, function() {
      $('#ticComplete').html("<i>Saved</i>");
      ct = newTic;
      showTic();
      callbackFromSaveTic()
    });
  } else {
    $.post(st, {
      fieldID: newTic,
      itemIDField: itemID
    }, function() {
      $('#ticComplete').html("<i>Saved</i>");
      ct = newTic;
      showTic();
      callbackFromSaveTic()
    });
  };
}

function find(selectedTic, ticObj) {
  $.each(ticObj, function(i, item) {
    if (item.tic.id == selectedTic) {
      foundTicObj = item;
      foundTic = true;
    }
  });
  if (!foundTic) {
    $.each(ticObj, function(i, item) {
      if (item.tic.children) {
        find(selectedTic, item.tic.children)
      }
    });
  }
  if (foundTic) {
    return foundTicObj;
  }
}

function getTic(whichTic) {
  if (whichTic.value == 'reset') {
    startTic();
  } else {
    var ticSelector = $("#" + fieldID);
    var selectedValue = whichTic.value;
    curSelectedTic = selectedValue;
    var selectedTitle = whichTic[whichTic.selectedIndex].title;
    var selectedLabel = whichTic[whichTic.selectedIndex].innerHTML;
    var done = false;
    var foundchilren = false;
    ticSelector.children().remove();
    if (selectedTitle.indexOf("(SSUTA)") != -1) {
      done = true;
      if (ws) {
        if (ub) {
          $('#ticComplete').html("&nbsp;&nbsp;<img style='cursor:pointer;' onclick='saveTic()' src='" + TaxCloudUrl + "imgs/24_go.gif' height='22' width='22' alt='Save' title='Save' border='0' align='absmiddle'/>");
        } else {
          $('#ticComplete').html("&nbsp;&nbsp;<b class='" + lc + "' style='cursor:pointer;' onclick='saveTic()'>Save</b>&nbsp;&nbsp;");
        }
      }
      if ((!ub) && ((ws) && (so))) {
        $('#ticComplete').html($('#ticComplete').html() + "|");
      }
      if (so) {
        var startOverText = "Start Over";
        if (saveTIC.length == 5) {
          startOverText = "Revert";
        }
        if ($('#ticComplete').html().indexOf('revert()') == -1) {
          if (ub) {
            $('#ticComplete').html($('#ticComplete').html() + "&nbsp;&nbsp;<img style='cursor:pointer;' onclick='revert()' src='" + TaxCloudUrl + "imgs/24_cancel.gif' height='22' width='22' title='" + startOverText + "' alt='" + startOverText + "' border='0' align='absmiddle'/>");
          } else {
            $('#ticComplete').html($('#ticComplete').html() + "&nbsp;&nbsp;<span class='" + lc + "' style='cursor:pointer;' onclick='revert()'>" + startOverText + "</span>");
          }
        }
      }
    }
    foundTic = false;
    var selectedObj = find(selectedValue, ticJSON);
    if (selectedObj.tic.children) {
      foundchilren = true;
      ticSelector.prepend('<option value="reset">-- Start Over --</option>');
      if (done) {
        ticSelector.append('<option selected="true" value="' + curSelectedTic + '">[ OK ]</option>');
      } else {
        ticSelector.append('<option selected="true">[ Select further ]</option>');
      }
      $.each(selectedObj.tic.children, function(i, item) {
        addOption(ticSelector, item.tic)
      });
      if (selectedLabel.indexOf("...") != -1) {
        selectedLabel = selectedLabel.substring(0, selectedLabel.length - 3)
      }
      $('#catList').append(selectedLabel + ":");
    } else {
      $('#catList').append(selectedLabel);
      $('#jqTicFinal').html("<input type='hidden' id='" + fieldID + "' value='" + selectedValue + "' />");
      $('#id_tic[name=tic]').val(selectedValue);
    }
  }
}

