// برای اینکه وقتی فیلتر کردیم بعد دوباره بخواهیم فیلتر کنیم فیلتر های قبلی پاک نشه
$(document).ready(
    function(){
    var urlparts = new URLSearchParams(Window.location.search);
    if (urlparts = ""){
        localStorage.clear();
        $("#filter_state").css("display", "none");
        } else {
            $("#filter_state").css("display", "inline_block");
        }
        $('input:checkbox').on('click', function(){
            var fav, favs = [];
            $('input:checkbox').each(function(){
                fav = { id : $(this).attr('id'), value: $(this).prop('checked')};
                favs.push(fav);
            })
            localStorage.setItem("favorites", JSON.stringify(favs)); 
        })
        var favorites = JSON.parse(localStorage.getItem('favorites'));
        for (var i = 0; i < favorites.length; i++){
            $('#' + favorites[i].id),prop('checked' , favorites[i].value);
        }
    }
);



// #---------------------------------------------------
// برای اینکه ردج قیمت را مشخص و کاما قرار دیهم 
function showVal(x){
    x = x.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
    document.getElementById('sel_price').innerText = x;

}
// #---------------------------------------------------
//##تابع برای حذف پارامترهای خط آدرس
function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2){
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;){

            if (pars[i].lastIndexOf(prefix, 0) != -1) {
                pars.splice(i, 1);
        }

        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
   
    return url;
}


//-------------------------------------------------------------------
//##تابع انتخاب مدل مرتب سازی محصولات 
function select_sort() {
    alert(test)
    var select_sort_value = $("#select_sort").val();
    // $("$select_sort").attr('selected', 'selected' );
    var url = removeURLParameter(window.Location.href, "sort_type");
    window.location = url + "&sort_type=" + select_sort_value;
    
}
// -------------------------shop_cart-----------------------------------
// ceate status shop_cart
status_of_shop_cart()
function status_of_shop_cart() {
    $.ajax({
        type: "GET",
        url : "/orders/status_of_shop_cart/",
        success: function(res) { 
            $("#indicator__value").text(res);
        }
    });
}
//-------------------------------------------------------------------
//##تابع برای افزودن کالا به سبد خرید
function add_to_shop_cart(product_id, qty){
    if (qty === 0) {
        qty = $("#product-quantity").val();
    }
    $.ajax({
        type: "GET",
        url : "/orders/add_to_shop_cart/",
        data :{
            product_id : product_id,
            qty :qty
        },
        success: function(res) {
            alert("کالا به سبد خرید اضافه شد");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}
//-------------------------------------------------------------------
// //##تابع برای حذف کالا از سبد خرید
function delete_form_shop_cart(product_id){
    $.ajax({
        type: "GET",
        url : "/orders/delete_form_shop_cart/",
        data :{
            product_id : product_id,
        },
        success: function(res) {
            alert("کالا مورد نظر حذف شد ");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
}

 
// create function update shop_cart(به روز رسانی)
function update_shop_cart(){
    var product_id_list = []
    var qty_list = []
    $("input[id^='qty_']").each(function(index) {
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    console.log(product_id_list);
    console.log(qty_list)
    $.ajax({
        type: "GET",
        url : "/orders/update_shop_cart/",
        data :{
            product_id_list : product_id_list,
            qty_list :qty_list,
        },
        success: function(res) {
  
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
    
}

// ----------------------------------------------------------------
function showCreateCommentForm(productId, commentId, slug) {
     
    $.ajax({
        type: "GET",
        url: "/csf/create_comment/" + slug ,
        data: {
            productId: productId,
            commentId: commentId,

        },
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    });
}
// ----------------------------------------------------------------
function showCreateCommentExpertForm(expertId, commentId, slug) {
     
    $.ajax({
        type: "GET",
        url: "/csf/create_commentexpert/" + slug ,
        data: {
            "expertId": expertId,
            "commentId": commentId,
        

        },
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    });
}
 
//----------------------------------------------------------------
function addScore(score, productId){
    var starRatings = document.querySelectorAll('.fa-star');
    starRatings.forEach(element => {
        element.classList.remove('checked'); 
    });
    for (let i = 1; i <= score; i++){
        const element = document.getElementById("star_" + i);
        element.classList.add('checked');
    }
 
    $.ajax({
        type: "GET",
        url: "/csf/add_score/",
        data:{
            productId: productId,
            score: score,
        },
        success: function(res) {
            alert(res);
        }
    });
    starRatings.forEach(element => {
        element.classList.add("disable");
    });
}
 
//----------------------------------------------------------------
function addScoreexpert(score_exp, expertId){
    var starRatings = document.querySelectorAll('.fa-star');
    starRatings.forEach(element => {
        element.classList.remove('checked'); 
    });
    for (let i = 1; i <= score_exp; i++){
        const element = document.getElementById("star_" + i);
        element.classList.add('checked');
    }
 
    $.ajax({
        type: "GET",
        url: "/csf/add_scoreexpert/",
        data:{
            expertId: expertId,
            score_exp: score_exp,
        },
        success: function(res) {
            alert(res);
        }

    });
    starRatings.forEach(element => {
        element.classList.add("disable");
    });
}
//----------------------------------------------------------------
function addToFavorites(productId) { 
    $.ajax({
        type: "GET",
        url: "/csf/add_to_favorite/",
        data:{
            productId: productId,
         
        },
        success: function(res) {
            alert(res);
        }

    });
}



//----------------------------------------------------------------
status_of_compare_list();
//----------------------------------------------------------------
function status_of_compare_list() {
    $.ajax({
        type: "GET",
        url : "/products/status_of_compare_list/",
        success: function(res) {
            if (Number(res) === 0 ) {
                $("#compare_count_icon").hide();
            } else {
                $("#compare_count_icon").show();
                $("#compare_count").text(res);
            } 
        },
    });
}

//----------------------------------------------------------------
function addToCompareList(productId, productGroupId) {
    $.ajax({
        type : "GET",
        url : "/products/add_to_compare_list/",
        data :{
            productId : productId,
            productGroupId: productGroupId,
        },
        success : function(res) {
            alert(res);
            status_of_compare_list();

        }
    });

}
//----------------------------------------------------------------
function deleteFormCompareList(productId) {
    $.ajax({
        type : "GET",
        url : "/products/delete_from_compare_list/",
        data :{
            productId: productId,
        },
        success: function(res) {
            alert('حذف با موفقیت انجام شد');
            $("#compare_list").html(res);
            status_of_compare_list();
        }
    });

}
//  scrollTo  

 

    // nav
    document.addEventListener('DOMContentLoaded', function() {  
        const menuItems = document.querySelectorAll('.menu-item');  
    
        menuItems.forEach(item => {  
            item.addEventListener('click', function(e) {  
                e.preventDefault(); // جلوگیری از بارگذاری مجدد صفحه  
                toggleSubMenu(item.nextElementSibling);  
            });  
        });  
    
        function toggleSubMenu(subMenu) {  
            if (subMenu.style.display === 'block') {  
                subMenu.style.display = 'none';  // پنهان کردن زیرمنو  
            } else {  
                subMenu.style.display = 'block';  // نمایش زیرمنو  
            }  
        }  
    });
// Dark Mode
document.getElementById('darkmode-toggle').addEventListener('change', function() {  
    if (this.checked) {  
        document.body.classList.remove('light-mode');  
        document.body.classList.add('dark-mode');  
    } else {  
        document.body.classList.remove('dark-mode');  
        document.body.classList.add('light-mode');  
    }  
});
 
	
// Show button when scrolling down  
window.onscroll = function() {  
    const button = document.getElementById('scroll-top');  
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {  
        button.style.display = "block";  
    } else {  
        button.style.display = "none";  
    }  
};  

// Scroll to top function  
function showContactInfo() {  
    var contactInfoDiv = document.getElementById('contactInfo');  
    var expireTag = document.getElementById('expireTag');  
    
    // اگر اطلاعات تماس قبلا نمایش داده شده باشد، آنها را پنهان می‌کنیم  
    if (contactInfoDiv.style.display === "block") {  
        contactInfoDiv.style.display = "none";  
        return;  
    } else {  
        contactInfoDiv.style.display = "block";  
    }  

    // با استفاده از AJAX اطلاعات تماس را بارگذاری می‌کنیم  
    var userId = "user-id-here"; // اینجا باید ID کاربر مربوطه را بنویسید  
    var xhr = new XMLHttpRequest();  
    xhr.open("GET", "/api/getContactInfo/" + userId, true);  
    xhr.onreadystatechange = function () {  
        if (xhr.readyState === 4 && xhr.status === 200) {  
            var result = JSON.parse(xhr.responseText);  
            if (result.subscription) {  
                // اگر کاربر فعال بود  
                expireTag.style.display = "none"; // پنهان کردن پیام منقضی  
                contactInfoDiv.style.display = "block"; // نمایش اطلاعات تماس  
                document.getElementById('contactFulltell').innerText = result.fullTell;  
                document.getElementById('contactMobile').innerText = result.mobile;  
                document.getElementById('contactWebAddress').innerText = result.webAddress;  
                document.getElementById('contactWebAddress').href = result.webAddress; // استفاده از آدرس وبی  
                document.getElementById('contactEmail').innerText = result.email;  
                document.getElementById('contactAddress').innerText = result.address;  
            } else {  
                // اگر کاربر غیرفعال بود  
                contactInfoDiv.style.display = "none"; // پنهان کردن اطلاعات تماس  
                expireTag.style.display = "block"; // نمایش پیام منقضی  
            }  
        } else if (xhr.readyState === 4) {  
            console.error("Error fetching contact info");  
        }  
    };  
    xhr.send();  
}

//   icon exit from site 
function RedirectToPage(id) {  
    // فرض کنید که id معادل یک URL خاص است.  
    // اینجا می‌توانید URL مربوطه را مشخص کنید.  
    const urlMap = {  
        1121: 'https://sanatpoya.com/logout'  
    };  

    const url = urlMap[id];  
    if (url) {  
        window.location.href = url;  
    } else {  
        console.error('Invalid ID:', id);  
    }  
}  

// اضافه کردن رویداد کلیک در کد HTML  
document.querySelector('.HeaderMenuItem').addEventListener('click', function() {  
    RedirectToPage(1121);  
});
// hide panel and logout
 
function logout() {  
    // مخفی کردن منوی پنل کاربری و گزینه خروج  
    document.querySelector('.topbar__item--link a[href="{% url \'accounts:userpanel\' %}"]').style.display = 'none';  
    document.querySelector('.topbar__item--link a[href="{% url \'accounts:logout\' %}"]').parentElement.style.display = 'none';  
}  
 
function toggleMenu() {  
    const navLinks = document.getElementById('nav-links');  
    navLinks.classList.toggle('active'); // فعال کردن یا غیرفعال کردن کلاس active  
}
 