const sheet=SpreadsheetApp.openById("구글시트 아이디");
function doPost(e){
  let p=e.parameter;
  if(p.method=="insert"){
    return ContentService.createTextOutput(insert(p));}
  return ContentService.createTextOutput("비정상적인 접근");
}
function insert(p){
  try{
    sheet.getSheetByName("유저정보").appendRow([p.id,p.pw,p.name,p.sex,p.year,p.month,p.day,p.ph,p.mbti]);
    return "회원가입 성공";
  }catch(e){
    return "회원가입 실패 : "+e.message;
  }
}