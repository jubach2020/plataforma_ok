$(document).ready(function () { 


   $('table.display tfoot th').each( function () {   
    var title = $(this).text();
    $(this).html( '<input type="text" placeholder="Filtrar.."   />' );       
    });

    var tabla_far = $('table.display').DataTable({               
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

$("#sinFiltroFarVer").hide();
$("#sinFiltroFar").hide();

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


   

   $("input[name=unirFar]").click(function(){   
       var checkedArray = [];
       var nifArray     = [];
       var unitArray    = []
       var descArray    = []
       var registro;
       var rows = $('#DataTables_Table_1').dataTable().fnGetNodes();    
           alert(rows);
       var j = 0;
       for(var i=0;i<rows.length;i++) { 
           var col = $(rows[i]).find('td:eq(4) input[type="checkbox"]');
           if (col.is(':checked')) {
               var idElem = col.attr("id");
               checkedArray.push(idElem); 
               var idNif = $(rows[i]).find('td:eq(0)').html();
               alert(idNif);
               nifArray[j] = String(idNif);

               var idUnit = $(rows[i]).find('td:eq(1)').html();
              
               unitArray[j] = String(idUnit);

               var desc = $(rows[i]).find('td:eq(2)').html();
               descArray[j] = String(desc);
               j=j+1;
        }        
    }
     
    var data =  "checkedArray="+checkedArray+"&nifArray="+nifArray+"&unitArray="+unitArray+"&descArray="+descArray;  
      $.ajax({
           type: "POST",
           url: "filtros-verticales/agregar-farmacias",  
           data: data,
           success: function(resp) {  
               for(var i=0;i<rows.length;i++) { 
                   var col = $(rows[i]).find('td:eq(4) input[type="checkbox"]');
                   if (col.is(':checked')) {
                     $(col).prop( "disabled", true );
                   }        
               }   
               location.reload();
              //$("#mensajeUnirFar").html("Datos agregados");
              //$("#mensajeUnirFar").fadeOut(5000);
           }
       });      
   });  

   $("input[name=borrarFar]").click(function(){
    var actual = $(this).parents("tr");
    var idElem = parseInt(this.id);
    var data = "id="+idElem;
    $.ajax({
        type: "POST",
        url: "/operaciones/mantenimientos/filtros-verticales/borrarFarVertical",  
        data: data,
        success: function(resp) {  
            actual.remove();
            location.reload();
        }
    });     
});
})    
       