const sheet=SpreadsheetApp.openById("구글시트 아이디");
function doPost(e){
  let p=e.parameter;
  sheet.getSheetByName("유저정보").appendRow([p.id,p.pw,p.name,p.sex,p.year,p.month,p.day,p.ph,p.mbti]);
  return ContentService.createTextOutput("회원가입 성공");
}