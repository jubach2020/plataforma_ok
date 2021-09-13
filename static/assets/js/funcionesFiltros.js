$(document).ready(function () {  

    $("input[name=borrarFiltro]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;    
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/filtros/borrarFiltro",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });     
    });

    $("input[name=editarFiltro]").click(function(){
      
        var idElem = parseInt(this.id);
        var nom = $("#filt"+ idElem +"").val();
        var data =  "id="+idElem+"&nom="+nom;
             
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/filtros/editarFiltro",  
            data: data,
                 success: function(resp) {  
                 $("#edicionMsgAgr"+ idElem +"").html("Datos editados");
                 $("#edicionMsgAgr"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });
        
    });  

    $('#listadoArtFil tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
    });

 
    var table_art = $('#listadoArtFil').DataTable({
        "destroy" : true,       
        "processing" : true,
        "dom": 'B<"float-left"i><"float-right"f>t<"float-left"l><"float-right"p><"clearfix">',
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
            $("#sinFiltro").hide();        
        }
        
    });

   //solo tiene en cuenta los de la página que está visible 
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
  
    

    $("input[name=unirArtFiltro]").click(function(){        
        var checkedArray = [];
        var labArray = [];
        var idFil = $('select[name=selectFiltro]').val();    
        var rows = $("#listadoArtFil").dataTable().fnGetNodes();
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

        var data =  "idFil="+idFil+"&checkedArray="+checkedArray+"&labArray="+labArray;        
        $.ajax({
            type: "POST",
            url: "/operaciones/mantenimientos/filtros-articulos/agrArtFiltro",  
            data: data,
            success: function(resp) {  
                for(var i=0;i<rows.length;i++) { 
                    var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                    if (col.is(':checked')) {
                      $(col).prop( "disabled", true );
                    }        
                }               
                //$("#mensajeUnir").html("Datos agregados");
                //$("#mensajeUnir").fadeOut(2000);
            }
        });      
    });      
        
    
    $("select[name=selectFiltro]").change(function() { 
        var selectAdd = $('select[name=selectFiltro]').val(); 
        if (selectAdd==0){
            var str = '<input  type="button" name="addFilButton" id="addFilButton" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Nuevo Filtro"/>';
            $("#divAddAgr").html('<div class="row"><div class="col-md-5"><input type="text" id="nuevoFil" name="nuevoFil" placeholder="Nuevo Filtro"/></div>'+
                                 '<div class="col-md-4">' + str + '</div></div>');
            $("input[name=addFilButton]").click(function(){
                var nuevoFil = $("#nuevoFil").val();
                var data =  "nuevoFil="+nuevoFil;
                $.ajax({
                        type: "POST",
                        url: "/operaciones/mantenimientos/filtros-articulos/agregarFilListado",  
                        data: data,
                        success: function(resp) { 
                            location.reload();
                          $("#nuevoFil").val(" ");
                          $("#divAddAgr").html("");
                          $('#div-tabla-filtro-art').show()
                        }
                });
            });
        } else {        
            var data = "idFil="+ selectAdd;
            //var texto = '<div class="row"><div class="col-md-5"><p>Este filtro ya tiene registros guardados</p></div>';
            //var botonStr = texto + '<div class="col-md-4"><input  type="button" name="verChecks" id="verChecks" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Ver listado"/>';
            var rows = $("#listadoArtFil").dataTable().fnGetNodes();
            var largo = rows.length;
            $.ajax({
                    type: "POST",
                    url: "/operaciones/mantenimientos/filtros-articulos/verFiltrosAgregados",  
                    data: data,
                    success: function(resp) {   
                        var content = resp.resultado;  
                        if (content.length > 0 ) {
                            //$("#divAddAgr").html(botonStr);
                            //$("input[name=verChecks]").click(function(){ 
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
                            $('#div-tabla-filtros-art').show();
                        } else { 
                            $('#div-tabla-filtros-art').hide();                     
                            $("#divAddAgr").html("");                            
                            for(var i=0;i<largo;i++) { 
                                var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                                if (col.prop("checked", true)) {
                                    col.prop("checked", false);
                                }
                            }
                            $('#div-tabla-filtros-art').show();
                        }
                    }                      
                });                             
            }                       
        }); 
})