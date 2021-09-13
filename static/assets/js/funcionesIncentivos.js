$(document).ready(function () {  

    $("input[name=borrarIncen]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;            
        $.ajax({
            type: "POST",
            url: "borrar-incentivo",  
            data: data,
            success: function(resp) {  
                actual.remove();
            }
        });    
    });

    $("input[name=editarIncen]").click(function(){      
        var idElem = parseInt(this.id);
        var imp = $("#incenImp"+ idElem +"").val();
        var data =  "id="+idElem+"&imp="+imp;             
        $.ajax({
            type: "POST",
            url: "editar-incentivo",  
            data: data,
                 success: function(resp) {  
                 $("#edicionMsgInc"+ idElem +"").html("Datos editados");
                 $("#edicionMsgInc"+ idElem +"").fadeOut(2000);
                location.reload();
            }
        });        
    });     


 /*funciones para el datatable de agrupación de artículos*/

 $('#listadoArt tfoot th').each( function () {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
});

    var table_art = $('#listadoArt').DataTable({
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

$("input[name=unirArtInc]").click(function(){        
    var checkedArray = [];
    var labArray = [];
    var idInc = $('select[name=selectInc]').val();    
    var idInc2 = $('select[name=selectInc2]').val();   
    var rows = $("#listadoArt").dataTable().fnGetNodes();
    var j = 0;
    for(var i=0;i<rows.length;i++) { 
        var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
        if (col.is(':checked')) {
            var idElem = col.attr("id");
            checkedArray.push(idElem); 
            var labArt = $(rows[i]).find('td:eq(2)').html();
            labArray[j] = String(labArt);
            j=j+1;
        }        
    }   
    if (idInc=='0' || idInc=='nuevo') {
        $("#mensajeAgregarInc").html("<h2>Debe seleccionar un incentivo</h2>");
        $("#mensajeAgregarInc").fadeOut(5000);
    } else {    
        var data =  "idInc="+idInc+"&idInc2="+idInc2+"&checkedArray="+checkedArray+"&labArray="+labArray;        
        $.ajax({
            type: "POST",
            url: "agrIncPost",  
            data: data,
            success: function(resp) {  
                for(var i=0;i<rows.length;i++) { 
                    var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                    if (col.is(':checked')) {
                    $(col).prop( "disabled", true );
                    }        
                }               
                $("#mensajeUnir").html("<h2>Datos agregados</h2>");
                $("#mensajeUnir").fadeOut(5000);
            }
        });    
    }  
});   



$("select[name=selectInc]").change(function() { 
    var selectAdd = $('select[name=selectInc]').val();     
    if (selectAdd=="nuevo"){
        var str = '<input  type="button" name="addIncButton" id="addIncButton" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Nuevo Incentivo"/>';
        $("#divAddInc").html('<div class="row"><div class="col-md-5"><input type="text" id="nuevoInc" name="nuevoInc" placeholder="Importe de Incentivo"/></div>'+
                             '<div class="col-md-4">' + str + '</div></div>');
        $("input[name=addIncButton]").click(function(){
            var nuevoInc = $("#nuevoInc").val();
            var data =  "nuevoInc="+nuevoInc;
            $.ajax({
                    type: "POST",
                    url: "agregarIncListado",  
                    data: data,
                    success: function(resp) { 
                        location.reload();
                      $("#nuevoInc").val(" ");
                      $("#divAddInc").html("");
                    }
            });
        });
    } else {         
        var data = "idInc="+ selectAdd;
        var texto = '<div class="row"><div class="col-md-5"><p>Este incentivo está asignado</p></div>';
        var botonStr = texto + '<div class="col-md-4"><input  type="button" name="verChecks" id="verChecks" class="btn btn-secondary float-right d-none d-sm-inline-block" value="Ver listado"/>';
        var rows = $("#listadoArt").dataTable().fnGetNodes();
        $.ajax({
                type: "POST",
                url: "verIncentivosAsignados",  
                data: data,
                success: function(resp) { 
                    var content = resp.resultado;
                    if (resp.resultado>0 ) {
                       $("#divAddInc").html(botonStr);
                    }                 
                    $("input[name=verChecks]").click(function(){ 
                        $("#divAddInc").html("");
                        var largo = rows.length;
                        for(var i=0;i<largo;i++) {
                            for (var j=0;j<content.lenght;j++){                             
                                var idJson = content[j];                                                     
                                var col = $(rows[i]).find('td:eq(9) input[type="checkbox"]');
                                if ((col.attr("id")==idJson)){
                                    col.prop("checked", true);
                                } 
                            }                               
                        }
                    }); 
                }                       
            });                             
        }                       
    }); 

  
});