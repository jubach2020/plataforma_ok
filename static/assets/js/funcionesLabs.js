$(document).ready(function () { 

  
  
    $('table.display tfoot th').each( function () {   
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );       
    });
  
    $('table.display').DataTable({               
            "dom": 'Bfrtip', 
            "responsive": true,
            
            "order": [[ 0, "desc" ]],
            "processing": true,
            "oLanguage": {
                "sProcessing": "<div id='loader'></div>"
            } ,  
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json",
                
            },         
          
            "initComplete": function () {
                this.api().columns().every( function () {
                var that = this;
                $( 'input', this.footer() ).on( 'keyup change', function () {
                    if ( that.search() !== this.value ) {                            
                        that
                           .search( this.value )
                           .draw();
                    }
                });             
            });                             
        }       
    });

    $('#sinfiltroVerLab').hide(); 
    $('#sinFiltroVertLab').hide();      
  

    $("input[name=agregarLabModal]").click(function(){      
        var codigo =  $(this).parents("tr").attr('id');   
        var vert    = $('select[name=selectVert]').val(); 
        var textoError = "<div class='alert alert-danger alert-dismissible fade show' role='alert'>"+ 
        "<strong>El Laboratorio ya está agregado a Laboratorios verticales</strong>"+ 
        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" + 
        "<span aria-hidden='true'>&times;</span></button></div>";
        
        $.ajax({ 
                    type: "POST",
                    url: "/operaciones/mantenimientos/laboratorios-verticales/verificarCodigo",  
                    data: "codigo="+codigo+"&vert="+vert,
                    success: function(resp) {  
                        if (resp == 'KO') { 
                        $("#agregarLabModal"+codigo+"").val('ERROR');               
                        $("#agregarLabModal"+codigo+"").prop('disabled', true);
                            $("#mensaje"+codigo+"").modal("show");
                            //$("mensajeCodigo"+codigo+"").html(textoError);                               
                        } else {
                            $("#agregarLabVertModal"+codigo).modal("show");                                                      
                        }
                    }
            });                               
    });

   /* $('select[name=selectVert]').change(function(){
        $('#labs').DataTable( {
            "dom": 'Bfrtip', 
            "responsive": false,
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
            },
            "order": [[ 0, "desc" ]],
            "initComplete": function () {
                this.api().columns().every( function () {
                var that = this;
                $( 'input', this.footer() ).on( 'keyup change', function () {
                    if ( that.search() !== this.value ) {                            
                        that
                           .search( this.value )
                           .draw();
                    }
                });             
            });                             
        }  
    })
     $('#labs tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );       
      });
      $('#sinfiltroVerLab').hide();     
});*/


    $("input[name=agregarLabVert]").click(function(){
        var idElem  = this.id;        
        var vert    = $('select[name=selectVert]').val(); 
        var nom     = $("#nomb"+ idElem +"").val();
        var color   = $("#color"+ idElem +"").val();  
        var data  =  "codigo="+idElem+"&nom="+nom+"&color="+color+"&vert="+vert;
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/laboratorios-verticales/agregarLabVertical",  
            data: data,
            success: function(resp) {                 
                $("#agregarLabVert"+idElem+"").fadeOut();
                location.reload();
            }
        });
    });  

    $("input[name=borrarLab]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/laboratorios-verticales/borrarLab",  
            data: data,
            success: function(resp) {  
                actual.remove();
                //location.reload();
            }
        });     
    });



   $("input[name=editarLab]").click(function(){        
        var idElem    = $("input[name=idEditar]").val();
        var codigo    = $("#codigo-"+ idElem +"").val();
        var nombre    = $("#nombre-"+ idElem +"").val();
        var vertical  = $("select[name=labVertical"+ idElem +"]").val(); 
        var color     = $("#color-"+ idElem +"").val();               
       
        var data      =  "Id="+idElem+"&codigo="+codigo+"&nombre="+nombre+"&vertical="+vertical+"&color="+color;
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/laboratorios-verticales/editarLab",  
            data: data,
            success: function(resp) {  
                location.reload();
            }
        });
    });    
});   