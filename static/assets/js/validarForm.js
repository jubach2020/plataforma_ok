$(document).ready(function () {    
         
        $.validator.setDefaults({
          submitHandler: function () {
            alert( "Formulario enviado exitosamente!" );
          }
        });
        $('#dptoForm').validate({
          rules: {
            dptoNom: {
              required: true,
              dptoNom: true,
            },             
          },
          messages: {
            dptoNom: {
              required: "Por favor ingrese el nombre del Departamento",
              dptoNom: "Por favor ingrese el nombre del Departamento"
            },        
          },
          errorElement: 'span',
          errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.form-group').append(error);
          },
          highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
          },
          unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
          }
        });    
    
        $.validator.setDefaults({
          submitHandler: function () {
            alert( "Formulario enviado exitosamente!" );
          }
        });
        $('#empForm').validate({
        rules: {
          empMail: {
            required: true,
            empMail: true,
          },
          empPass: {
            required: true,
            minlength: 5
          },   
          empNom: {
            required: true,
            empNom: true,
          },
          nomUsuario:{
            required: true,
            nomUsuario: true
          }    
        },
        messages: {
          empMail: {
            required: "Por favor ingrese un email válido",
            empMail:  "Por favor ingrese un email válido"
          },
          empNom: {
            required: "Por favor ingrese el nombre del empleado",
            empNom:   "Por favor ingrese el nombre del empleado"
          },
          nomUsuario: {
            required:   "Por favor ingrese el nombre de usuario",
            nomUsuario: "Por favor ingrese el nombre de usuario"
          },
          empPass: {
            required:  "Por favor ingrese una contraseña válida",
            minlength: "Su password debe tener al menos 5 caracteres"
          },        
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
          error.addClass('invalid-feedback');
          element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        }
      });
    
        $.validator.setDefaults({
          submitHandler: function () {
            alert( "Formulario enviado exitosamente!" );
          }
        });
        $('#rolForm').validate({
        rules: {       
          idRol: {
            required: true,
            idRol: true,
          },
          nomRol:{
            required: true,
            nomRol: true
          }    
        },
        messages: {
          idRol: {
            required: "Por favor ingrese id del rol",
            idRol:  "Por favor ingrese id del rol"
          },
          nomRol: {
            required: "Por favor ingrese el nombre del rol",
            nomRol:   "Por favor ingrese el nombre del rol"
          },            
        },
        errorElement: 'span',
        errorPlacement: function (error, element) {
          error.addClass('invalid-feedback');
          element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
          $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
          $(element).removeClass('is-invalid');
        }
      });
     
  
   
      $("#pass").keyup(checkPasswordMatch);    
  
      $("#pass2").keyup(checkPasswordMatchReg); 
   
})
    
function checkPasswordMatch() {
      var password = $("#empPass").val();
      var confirmPassword = $("#empPass2").val();
      if (password != confirmPassword)
          $("#CheckPasswordMatch").html("Passwords does not match!");
      else
          $("#CheckPasswordMatch").html("Passwords match.");
}      

function checkPasswordMatchReg() {
  var password = $("#pass").val();
  var confirmPassword = $("#pass2").val();
  if (password != confirmPassword) {
    $("#CheckPasswordMatchReg").css({'color':'red'});
    $("#CheckPasswordMatchReg").html("Las contraseñas son diferentes");
  } else {
      $("#CheckPasswordMatchReg").css({'color':'green'});
      $("#CheckPasswordMatchReg").html("Contraseñas iguales");
  }
}                 
                          
    
   

   