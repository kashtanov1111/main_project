$(document).ready(function(){
  $.ajaxSetup({
    headers: {
      "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
    }
  })
    var contactForm = $('.contact-form')
    var contactFormMethod = contactForm.attr('method')
    var contactFormEndPoint = contactForm.attr('action')
    function displaySubmitting(submitBtn, defaulttext, doSubmit){
      if (doSubmit){
        submitBtn.css('width', '200px')
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
      } else {
        submitBtn.html(defaulttext)
      }
    }

    contactForm.submit(function(event){
      event.preventDefault()
      var contactFormData = contactForm.serialize()
      var thisForm = $(this)
      var contactFormSubmitBtn = contactForm.find("[type='submit']")
      var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
      displaySubmitting(contactFormSubmitBtn, '', true)
      $.ajax({
        method: contactFormMethod,
        url: contactFormEndPoint,
        data: contactFormData,
        success: function(data){
          contactForm[0].reset()
          $.alert({
            title: "Success!",
            content: data.message ,
            theme: 'modern',
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          }, 500)
        },
        error: function(errorData){
          console.log(errorData.responseJSON)
          var jsonData = errorData.responseJSON
          var msg = ''

          $.each(jsonData, function(key, value){
            msg += key + ': ' + value[0].message + '<br>'
          })

          $.alert({
            title: "Oops!",
            content: msg,
            theme: 'modern',
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          }, 500)
        }
      })
    })

    
    
    var typingTimer
    var typingInterval = 500

    var searchForm = $('.search-form')
    var searchBtn = searchForm.find("[type='submit']")
    var searchInput = searchForm.find("[name='q']")

    searchInput.keyup(function(event){
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch(), typingInterval)
    })

    searchInput.keydown(function(event){
      clearTimeout(typingTimer)
    })

    function performSearch(){
      searchBtn.css('width', '200px')
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
      var query = searchInput.val()
      setTimeout(function(){
        window.location.href = '/products/search/?q=' + query
      }, 1000)
    }

    var productForm = $('.form-product-ajax')

    productForm.submit(function(event){
      event.preventDefault();
      var thisForm = $(this)
      var actionEndpoint = thisForm.attr('data-endpoint')
      var httpMethod = thisForm.attr('method')
      var formData = thisForm.serialize()
      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find('.submit-span')
          if (data.added) {
            submitSpan.html("In cart <button class='btn btn-link' type='submit'>Remove?</button>")
          } else {
            submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
          }
          var navbarCount = $('.navbar-cart-count')
          navbarCount.text(data.cartItemCount)
          var currentPath = window.location.href
          if (currentPath.indexOf('cart') != -1) {
            refreshCart()
          }
        },
        error: function(errorData){
          $.alert({
            title: "Oops!",
            content: 'An error occured',
            theme: 'modern',
          })
          console.log('errorre')
          console.log(errorData)
        },
      })
    })
    function refreshCart(){
      console.log('In current cart')
      var cartTable = $('.cart-table')
      var cartBody = cartTable.find('.cart-body')
      var productRows = cartBody.find('.cart-products')

      var refreshCartUrl = '/api/cart/'
      var refreshCartMethod = 'GET'
      var currentUrl = window.location.href
      var data = {}
      $.ajax({
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){
          console.log('success')
          console.log(data)
          var hiddenCartItemRemovedForm = $('.cart-item-remove-form')
          if (data.products.length > 0){
            productRows.html("")
            i = data.products.length
            $.each(data.products, function(index, value){
              var newCartItemRemove = hiddenCartItemRemovedForm.clone()
              newCartItemRemove.css('display', 'block')
              newCartItemRemove.find('.cart-item-product-id').val(value.id)
              cartBody.prepend("<tr><th scope=\"row\">" + i +
                 "</th><td><a style='text-decoration:none;' href='"+ 
                  value.url + "'>"+ value.title + "</a>" + newCartItemRemove.html()
                    + "</td><td>"+ value.price + "</td></tr>")
              i--
            })
            cartBody.find('.cart-subtotal').text(data.subtotal)
            cartBody.find('.cart-total').text(data.total)
          } else {
            window.location.href = currentUrl
          }
        },
        error: function(errorData){
          $.alert({
            title: "Oops!",
            content: 'An error occured',
            theme: 'modern',
          })
          console.log('error')
          console.log(errorData)
        }
      })

    }

    
  })