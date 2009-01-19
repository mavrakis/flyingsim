/***************************/
//@Author: Adrian "yEnS" Mato Gondelle & Ivan Guardado Castro
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!					
/***************************/

$(document).ready(function(){
	$(".menu > li.fade").click(function(e){
		//alert(e.target.id);
		switch(e.target.id){
			case "tab1":
				//change status & style menu
				$("#tab1").addClass("active");
				$("#tab2").removeClass("active");
				$("#tab4").removeClass("active");
				$("#tab3").removeClass("active");
				//display selected division, hide others
				$("div.tab1").fadeIn();
				$("div.tab2").css("display", "none");
				$("div.tab4").css("display", "none");
				$("div.tab3").css("display", "none");
			break;
			case "tab2":
				//change status & style menu
				$("#tab1").removeClass("active");
				$("#tab2").addClass("active");
				$("#tab4").removeClass("active");
				$("#tab3").removeClass("active");
				//display selected division, hide others
				$("div.tab2").fadeIn();
				$("div.tab1").css("display", "none");
				$("div.tab4").css("display", "none");
				$("div.tab3").css("display", "none");
			break;
			case "tab3":
				//change status & style menu
				$("#tab1").removeClass("active");
				$("#tab3").addClass("active");
				$("#tab2").removeClass("active");
				$("#tab4").removeClass("active");
				//display selected division, hide others
				$("div.tab3").fadeIn();
				$("div.tab1").css("display", "none");
				$("div.tab4").css("display", "none");
				$("div.tab2").css("display", "none");
			break;			
			
			case "tab4":
				//change status & style menu
				$("#tab1").removeClass("active");
				$("#tab2").removeClass("active");
				$("#tab4").addClass("active");
				$("#tab3").removeClass("active");
				//display selected division, hide others
				$("div.tab4").fadeIn();
				$("div.tab1").css("display", "none");
				$("div.tab2").css("display", "none");
				$("div.tab3").css("display", "none");
			break;
		}
		//alert(e.target.id);
		return false;
	});
});