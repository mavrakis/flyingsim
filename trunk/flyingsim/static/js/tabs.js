/***************************/
//@Author: Adrian "yEnS" Mato Gondelle & Ivan Guardado Castro
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!					
/***************************/

$(document).ready(function(){
	$(".menu > li").click(function(e){
		switch(e.target.id){
			case "flight":
				//change status & style menu
				$("#flight").addClass("active");
				$("#airports").removeClass("active");
				$("#about").removeClass("active");
				$("#users").removeClass("active");
				//display selected division, hide others
				$("div.flight").fadeIn();
				$("div.airports").css("display", "none");
				$("div.about").css("display", "none");
				$("div.users").css("display", "none");
			break;
			case "airports":
				//change status & style menu
				$("#flight").removeClass("active");
				$("#airports").addClass("active");
				$("#about").removeClass("active");
				$("#users").removeClass("active");
				//display selected division, hide others
				$("div.airports").fadeIn();
				$("div.flight").css("display", "none");
				$("div.about").css("display", "none");
				$("div.users").css("display", "none");
			break;
			case "users":
				//change status & style menu
				$("#flight").removeClass("active");
				$("#users").addClass("active");
				$("#airports").removeClass("active");
				$("#about").removeClass("active");
				//display selected division, hide others
				$("div.users").fadeIn();
				$("div.flight").css("display", "none");
				$("div.about").css("display", "none");
				$("div.airports").css("display", "none");
			break;			
			
			case "about":
				//change status & style menu
				$("#flight").removeClass("active");
				$("#airports").removeClass("active");
				$("#about").addClass("active");
				$("#users").removeClass("active");
				//display selected division, hide others
				$("div.about").fadeIn();
				$("div.flight").css("display", "none");
				$("div.airports").css("display", "none");
				$("div.users").css("display", "none");
			break;
		}
		//alert(e.target.id);
		return false;
	});
});