function doGet(e) {
  return handleResponse(e);
}

var d = Utilities.formatDate(new Date(), "GMT+7", "dd/MM/yyyy/HH/mm/ss")

const token = d.split('/')

var SHEET_NAME = `Tháng ${token[1]}/${token[2]}`;

var SCRIPT_PROP = PropertiesService.getScriptProperties();

function handleResponse(e) {
  var lock = LockService.getPublicLock();
  lock.waitLock(30000);

  try {
    var doc = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = doc.getSheetByName(SHEET_NAME);
    if (!sheet) {
      totalSheets = doc.getNumSheets()
      sheet = doc.insertSheet(totalSheets);
      sheet.setName(SHEET_NAME);
      sheet.getRange(1, 1, 1, 4).setValues([["time", "item", "price", "buyer"]]);
    }
    var headers = sheet.getRange(1, 1, 1, 4).getValues()[0];
    var nextRow = sheet.getLastRow() + 1;
    var row = [];

    for (i in headers) {
      if (headers[i] === "time") {
        row.push(`${token[3]}:${token[4]}:${token[5]} ${token[0]}/${token[1]}/${token[2]}`)
      } else {
        row.push(e.parameter[headers[i]]);
      }
    }

    sheet.getRange(nextRow, 1, 1, row.length).setValues([row]);

    return ContentService
      .createTextOutput(JSON.stringify({ "result": "success", "row": nextRow }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (e) {
    return ContentService
      .createTextOutput(JSON.stringify({ "result": "error", "error": e.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function setup() {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  SCRIPT_PROP.setProperty("key", doc.getId());
}

function test() {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = doc.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = doc.insertSheet();
    sheet.setName(SHEET_NAME);
    sheet.getRange(1, 1, 1, 4).setValues([["time", "item", "price", "buyer"]]);
  }
}
