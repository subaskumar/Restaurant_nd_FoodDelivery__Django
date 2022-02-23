const showModal = (mymodal) => {
  document.getElementById(mymodal).style.display='block'
  document.body.classList.add("stop-scrolling");  
}

const hideModal = (mymodal) => {
  document.getElementById(mymodal).style.display='none'
  document.body.classList.remove("stop-scrolling");
  $(".contacts").trigger('reset');
  $(".error").empty()
}

const OpenCartModal = (mymodal) => {

  const url = 'get_cart_item/'
  $.ajax({
    type: 'GET',
    url: url,
    data: {},
    dataType: 'json',
    success: function(response) {
        document.getElementById('my_cart_item').innerHTML = response.cart
        document.getElementById(mymodal).style.display='block'
        document.body.classList.add("stop-scrolling");
      },
      error:function(response) {
        document.getElementById("snackbar").classList.add("show");
        document.getElementById("snackbar").innerHTML = "<i class='fa fa-exclamation-circle'></i>  Login Required...!  ";
        setTimeout(function(){ 
          document.getElementById("snackbar").classList.remove("show") }, 5000);
      }
    })
}

const OpenOrderModal = (mymodal) =>{
  document.getElementById(mymodal).style.display='block'
  document.body.classList.add("stop-scrolling");
}

const placeOrder = () =>{

  const url = 'order_item/'
  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'json',
    success: function(response) {
        document.getElementById('my_cart_item').innerHTML = response.Order_Form  
      }
    })
}

// submit user details for place order
function submit_details(){
  var serializedData = $('form').serialize();
  console.log(serializedData)
    const url = 'order_item/'
    $.ajax({
      type: 'POST',
      url: url,
      data: serializedData,
      dataType: 'json',
      success: function(response) {
        hideModal('CartModal')
        if(response.message){
          document.getElementById("snackbar").classList.add("show");
          document.getElementById("snackbar").innerHTML = `<i class='fa fa-check-circle'></i>  ${response.message}`;
          setTimeout( async function(){ 
            document.getElementById("snackbar").classList.remove("show")
            await window.location.reload()
          }, 3000);
          }
      },
    });
}

// Ajax Registration form

$('#register').submit(function(event){
  event.preventDefault()

  const url = $(this).attr('action')
  var serializedData = $(this).serialize();
  $.ajax({
      type: 'POST',
      url: url,
      data: serializedData,
      dataType: 'json',
      success: function(response) {
          if(response.message == "Successfull"){
            document.getElementById("snackbar").classList.add("show");
            document.getElementById("snackbar").innerHTML = "<i class='fa fa-check-circle'></i>  You Registred Successfully  ";
            setTimeout(function(){ 
              document.getElementById("snackbar").classList.remove("show") }, 5000);

            document.getElementById("SignUpModal").style.display = 'none';
            document.getElementById("LoginModal").style.display = 'block'

          }
          else if(response.registererror.email){
            console.log(response.registererror.email)
            document.getElementById("RegError").innerHTML = response.registererror.email;
          }
          else if(response.registererror.password2){
            $("#RegError").text(response.registererror.password2);

          }
        },
        error:function(response) {
          document.getElementById("snackbar").classList.add("show");
          document.getElementById("snackbar").innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.  ";
          setTimeout(function(){ 
            document.getElementById("snackbar").classList.remove("show") }, 5000);
        }
  });
});

// Ajax LogIn Form

$('#login').submit(function(event){

  event.preventDefault()
  const url = $(this).attr('action')
  var serializedData = $(this).serialize();
  $.ajax({
      type: 'POST',
      url: url,
      data: serializedData,
      dataType: 'json',
      success: function(response) {
          if(response.message == "loginSucessfully"){
            document.getElementById("snackbar").classList.add("show");
            document.getElementById("snackbar").innerHTML = "<i class='fa fa-check-circle'></i>  LogIn Successfully  ";
            setTimeout(async function(){ 
              document.getElementById("snackbar").classList.remove("show")
              await window.location.reload() }, 3000);
              hideModal('LoginModal')
          }
          else if(response.formerror.email){
            console.log(response.formerror.email)
            $("#LogInError").text(response.formerror.email);
          }
          else if(response.formerror.password){
            $("#LogInError").text(response.formerror.password);

          }
        },
        error:function(response) {
          document.getElementById("snackbar").classList.add("show");
          document.getElementById("snackbar").innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.  ";
          setTimeout(function(){ 
            document.getElementById("snackbar").classList.remove("show") }, 5000);   
        }
  });
});

const Add_To_Cart = (id) => {
  let cart_item = $('#add_cart_item').text()
  const url = 'add_to_cart/'

  $.ajax({
    type: 'GET',
    url: url,
    data: {'Item_id': id},
    dataType: 'json',
    success: function(response) {
      if(response.message == 'add'){
        $('#add_cart_item').text(parseInt(cart_item) + 1)
      }
    },
    error:function(response) {
      document.getElementById("snackbar").classList.add("show");
      document.getElementById("snackbar").innerHTML = "<i class='fa fa-exclamation-circle'></i>  Login Required...!  ";
      setTimeout(function(){ 
        document.getElementById("snackbar").classList.remove("show") }, 5000);
    }
  })
}

const remove_item = (id) => {

  let cart_item = $('#add_cart_item').text()
  const url = `/remove_to_cart/${id}`

  $.ajax({
    type: 'GET',
    url: url,
    data: {},
    dataType: 'json',
    success: function(response) {
      document.getElementById('my_cart_item').innerHTML = response.cart
      $('#add_cart_item').text(parseInt(cart_item) - 1 )
    },
    error:function(response) {
      document.getElementById("snackbar").classList.add("show");
      document.getElementById("snackbar").innerHTML = "<i class='fa fa-exclamation-circle'></i>  Something's not right. Please try again.  ";
      setTimeout(function(){ 
        document.getElementById("snackbar").classList.remove("show") }, 5000);
    }
  })
}

const update_quantity = (cItem_id,pm) => {

  const url = "Plus_minus_quantity/"
  const input_id = 'quantity_input' + cItem_id

  $.ajax({
    type: 'GET',
    url: url,
    data: {
      'cItem_id': cItem_id,
      'PM': pm
    },
    success: function(response) {

      document.getElementById(input_id).value = response.quantity
      document.getElementById("total_price").innerHTML = response.total_price
    },
  })
}


// For style and Annimation
function main() {

  (function () {
     'use strict';
     
      $('a.page-scroll').click(function() {
          if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
              $('html,body').animate({
                scrollTop: target.offset().top - 40
              }, 900);
              return false;
            }
          }
        });
      // Show Menu on Book
      $(window).bind('scroll', function() {
          var navHeight = $(window).height() - 500;
          if ($(window).scrollTop() > navHeight) {
              $('.navbar-default').addClass('on');
          } else {
              $('.navbar-default').removeClass('on');
          }
      });
  
      $('body').scrollspy({ 
          target: '.navbar-default',
          offset: 10
      });
    // Hide nav on click
    $(".navbar-nav li a").click(function (event) {
      // check if window is small enough so dropdown is created
      var toggle = $(".navbar-toggle").is(":visible");
      if (toggle) {
        $(".navbar-collapse").collapse('hide');
      }
    });
    
      // Portfolio isotope filter
      $(window).load(function() {
          var $container = $('.portfolio-items');
          $container.isotope({
              filter: '*',
              animationOptions: {
                  duration: 750,
                  easing: 'linear',
                  queue: false
              }
          });
          $('.cat a').click(function() {
              $('.cat .active').removeClass('active');
              $(this).addClass('active');
              var selector = $(this).attr('data-filter');
              $container.isotope({
                  filter: selector,
                  animationOptions: {
                      duration: 750,
                      easing: 'linear',
                      queue: false
                  }
              });
              return false;
          });
      });
      // Nivo Lightbox 
      $('.portfolio-item a').nivoLightbox({
              effect: 'slideDown',  
              keyboardNav: true,                            
          });
  }());
  }
  main();