$(document).ready(function () {  

  
 /*funciones para el datatable de agrupación de artículos*/

 
 
    var table_art = $('#listadoAsignacionCuotas').DataTable({
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
$('#listadoAsignacionCuotas tfoot th').each( function () {
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Filtrar.."   />' );
});

    $('input[name=asignarCuota]').click(function(){
        var selectLab  = $('select[name=selectLab]').val();
        var selectFar  = $('select[name=selectFar]').val();
        var base = $('input[name=base]').val();
        var total = $('input[name=total]').val();
        var cuota = $('input[name=cuota]').val();
        var cuotaDos = $("#cuotaDos").val();    
        var data =  "selectLab="+selectLab+"&selectFar="+selectFar+"&total="+total+"&cuota="+cuota+"&base="+base+"&cuotaDos="+cuotaDos; 
        $.ajax({
            type: "POST",
            url: "/operaciones/trabajos/asignacion-cuotas",  
            data: data,
            success: function(resp) { 
                if (resp='OK') {
                    location.reload();
                }
                             
            }
        });
    })

    
    $("input[name=editarAsig]").click(function(){
        var idElem = $("input[name=idEditar]").val();       
      
        var farHidden   = $("#farHidden"+ idElem +"").val();
        var labHidden   = $("#labHidden"+ idElem +"").val();
        var base        = $("#base"+ idElem +"").val();
        var total       = $("#total"+ idElem +"").val();  
        var cuota       = $("#cuota"+ idElem +"").val();   
        var cuotaDos    =  $("#cuotaDos"+ idElem +"").val(); 
        var data =  "idEditar="+idElem+"&selectLab="+lab+"&selectFar="+far+"&base="+base+"&cuota="+cuota+"&idLab="+labHidden+"&idUnit="+farHidden+"&total="+total+"&cuotaDos="+cuotaDos; 
        $.ajax({
            type: "POST",
            url: "/operaciones/trabajos/asignacion-cuotas/editar",  
            data: data,
            success: function(resp) { 
                 $("#edicionMsgInc"+ idElem +"").html("Datos editados");
                 $("#edicionMsgInc"+ idElem +"").fadeOut(2000);          
            }
        });
    })

    
    $("input[name=borrarAsigCuota]").click(function(){
        var selectLab  = $('select[name=selectLab]').val();
        var selectFar  = $('select[name=selectFar]').val();
        var base        = $("#base").val();
        var total       = $("#total").val();      
        var cuota       = $("#cuota").val();   
        var cuotaDos    = $("#cuotaDos").val();      
        var data =  "selectLab="+selectLab+"&selectFar="+selectFar+"&base="+base+"&total="+total+"&cuota="+cuota+"&cuotaDos="+cuotaDos; 
        $.ajax({
            type: "POST",
            url: "/operaciones/trabajos/asignacion-cuotas/borrar-cuota",  
            data: data,
            success: function(resp) { 
              location.reload();              
            }
        });
    });

    $("input[name=borrarAsig]").click(function(){
        var actual = $(this).parents("tr");
        var idElem = parseInt(this.id);
        var data = "id="+idElem;
        $.ajax({
            type: "POST",
            url: "/operaciones/trabajos/asignacion-cuotas/borrarAsig",  
            data: data,
            success: function(resp) {  
                actual.remove();
                location.reload();
            }
        });     
    });


});