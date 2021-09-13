$(document).ready(function () {  
    

    $("input[name=borrarEmp]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;    
        $.ajax({
            type: "POST",
            url: "borrarEmpleado",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });     
    });

    $("input[name=borrarRol]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
        $.ajax({
            type: "POST",
            url: "borrarRol",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });     
    });

    $("input[name=borrarDpto]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
        $.ajax({
            type: "POST",
            url: "borrarDpto",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });     
    });

    $("input[name=borrarAgrup]").click(function(){

        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
                
        $.ajax({
            type: "POST",
            url: "borrarAgr",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });    
         
    });

    $("input[name=editarEmpleado]").click(function(){
        
        var idElem = parseInt(this.id);
        var empNom = $("#empNom"+ idElem +"").val();
        var nomUsuario = $("#nomUsuario"+ idElem +"").val();
        var empMail = $("#empMail"+ idElem +"").val();
        var idRol = $("#empRol"+ idElem +"").val();
        var idDpto = $("#empDpto"+ idElem +"").val();

        var data =  "id="+idElem+"&empNom="+empNom+"&nomUsuario="+nomUsuario+"&empMail="+empMail+"&idRol="+idRol+"&idDpto="+idDpto;
      
        $.ajax({
            type: "POST",
            url: "editarEmpleado",  
            data: data,
            success: function(resp) {  
                 $("#edicionMsgEmp"+ idElem +"").html("Datos editados");
                 $("#edicionMsgEmp"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });
    });  

    $("input[name=editarDpto]").click(function(){
        
        var idElem = parseInt(this.id);
        var nomDpto = $("#dptoNom"+ idElem +"").val();
        var descDpto = $("#dptoDesc"+ idElem +"").val();       
        var data =  "id="+idElem+"&nomDpto="+nomDpto+"&descDpto="+descDpto;
      
        $.ajax({
            type: "POST",
            url: "editarDpto",  
            data: data,
            success: function(resp) {  
                 $("#edicionMsgDpto"+ idElem +"").html("Datos editados");
                 $("#edicionMsgDpto"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });
    });  

    $("input[name=editarRol]").click(function(){
        
        var idElem = parseInt(this.id);
        var nomRol = $("#nomRol"+ idElem +"").val();
        var data =  "idRol="+idElem+"&nomRol="+nomRol;
      
        $.ajax({
            type: "POST",
            url: "editarRol",  
            data: data,
            success: function(resp) {  
                 $("#edicionMsgRol"+ idElem +"").html("Datos editados");
                 $("#edicionMsgRol"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });
    });  

    $("input[name=editarAgrup]").click(function(){
      
        var idElem = parseInt(this.id);
        var nom = $("#agrup"+ idElem +"").val();
        var color = $("#color"+ idElem +"").val();
        var data =  "id="+idElem+"&nom="+nom+"&color="+color;
             
        $.ajax({
            type: "POST",
            url: "editarAgrup",  
            data: data,
                 success: function(resp) {  
                 $("#edicionMsgAgr"+ idElem +"").html("Datos editados");
                 $("#edicionMsgAgr"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });
        
    });     
   
    $("#submitEmp").click(function(){
        location.reload();
    });

    /*funciones para el datatable de agrupación de artículos*/

   

    $("input[name=submitFileUpload").click(function(){  
       var  data='';
        $.ajax({
            type: "POST",
            url: "/uploadAgrupaciones",  
            data: data,
            success: function(resp) {  
                 $("#mensajeUpload").html("Archivo subido correctamente");
                 $("#mensajeUpload").fadeOut(6000);
            }
        })
    });
  
     
    var table_art = $('#listadoArt').DataTable({      
        //serverSide: true,
        //ajax: "/operaciones/mantenimientos/agrupacion/get-articulos",
        "destroy" : true,       
        "processing" : true,
        "pageLength": 10,
        retrieve: true,
        dom: 'Blfrtip',
        "responsive": true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
        },        
        "order": [[ 1, "asc" ]],
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
            $("#sinFiltro").hide();        
        }        
    });  
    $('#listadoArt tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
    });

    

    $('#select_all').click(function() {
        if ($('#select_all').is(':checked')){
            $("input[type=checkbox]").each(function(index, check ){
                $("input[type=checkbox]").prop('checked', true);
            });
            //var checkboxes = $(this).closest('form').find(':checkbox').not($(this));
            //checkboxes.prop('checked', true);
        }
         else {
            $("input[type=checkbox]").each(function(index, check ){
                $("input[type=checkbox]").prop('checked', false);
            });
            //var checkboxes = $(this).closest('form').find(':checkbox').not($(this));
            //checkboxes.prop('checked', false);
         }
    });

    $(".cerrarModal").click(function(){
        $("#mensajeError").modal('hide')
    });

    $("input[name=unirArtAgr]").click(function(){      
        var idAgr = $('select[name=selectAgr]').val();  
        if (idAgr==0) {
            $("#mensajeError").modal("show");
        } else {
            var checkedArray = [];
            var labArray = [];
            
            var rows = $("#listadoArt").dataTable().fnGetNodes();
            var j = 0;
            for(var i=0;i<rows.length;i++) { 
                var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                if (col.is(':checked')) {
                    var idElem = col.attr("id");
                    checkedArray.push(idElem); 
                    var idLab = $(rows[i]).find('td:eq(2)').html();
                    labArray[j] = String(idLab);
                    j=j+1;
                }        
            }

            var data =  "idAgr="+idAgr+"&checkedArray="+checkedArray+"&labArray="+labArray;        
            $.ajax({
                type: "POST",
                url: "agrArtPost",  
                data: data,
                success: function(resp) {  
                    for(var i=0;i<rows.length;i++) { 
                        var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                        if (col.is(':checked')) {
                        $(col).prop( "disabled", true );
                        }        
                    }               
                    $("#mensajeUnir").html("Artículos agrupados");
                    $("#mensajeUnir").fadeOut(5000);
                }
            });    
        }  
    });      
  
    
    $("select[name=selectAgr]").change(function() { 
        var selectAdd = $('select[name=selectAgr]').val();   
        if (selectAdd==1){
            var str = '<input  type="button" name="addAgrButton" id="addAgrButton" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Nueva Agrupación"/>';
                        $("#divAddAgr").html('<div class="row"><div class="col-md-5"><input type="text" id="nuevaAgr" name="nuevaAgr" placeholder="Nueva Agrupación"/></div>'+
                       '<div class="col-md-4">' + str + '</div></div>');
            $("input[name=addAgrButton]").click(function(){
                var nuevaAgr = $("#nuevaAgr").val();
                var data =  "nuevaAgr="+nuevaAgr;
                $.ajax({
                        type: "POST",
                        url: "agregarAgrListado",  
                        data: data,
                        success: function(resp) { 
                          location.reload();
                          $("#nuevaAgr").val(" ");
                          $("#divAddAgr").html("");
                          $('#div-tabla-agrupa-art').show(); 
                        }
                });
            });
        } else {         
            var data = "idAgr="+ selectAdd;
         
            //var texto = '<div class="row"><div class="col-md-5"><p>Esta agrupación ya tiene registros guardados</p></div>';
            //var botonStr = texto + '<div class="col-md-4"><input  type="button" name="verChecks" id="verChecks" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Ver listado"/>';
            var rows = $("#listadoArt").dataTable().fnGetNodes();
            var largo = rows.length;
            $.ajax({
                    type: "POST",
                    url: "verAgrupacionesAgregadas",  
                    data: data,
                    success: function(resp) {   
                        var content = resp.resultado;  
                        for(var i=0;i<largo;i++) { 
                            var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                            col.prop("checked", false);
                        }
                        if (content.length > 0 ) {       
                        //$("#divAddAgr").html(botonStr);                        
                        $("#divAddAgr").html("");                         
                           for(var i=0;i<largo;i++) { 
                               for (var j=0;j<content.length;j++){  
                                   var idJson = content[j]['cn'];                               
                                   var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                                   if ((col.attr("id")==idJson)){
                                       col.prop("checked", true);
                                    } 
                                }                               
                            } 
                            $('#div-tabla-agrupa-art').show();                                                  
                        } else {       
                            $('#div-tabla-agrupa-art').hide();                     
                            $("#divAddAgr").html("");                            
                            for(var i=0;i<largo;i++) { 
                                var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                                if (col.prop("checked", true)) {
                                    col.prop("checked", false);
                                }
                            }
                            $('#div-tabla-agrupa-art').show();
                        }
                        //$("input[name=verChecks]").click(function(){ 
                           // $("#divAddAgr").html("");                           
                        //}); 
                    }                       
                });                             
            }                       
        }); 
});