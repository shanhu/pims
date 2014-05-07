$(function(){
    
    $("#sidebar > li > a").on("click",function(){
        
            $("#sidebar > li").each(function(){
                $(this).removeClass("active");
            });
            $(this).parent().addClass("active");
    });



    
});
