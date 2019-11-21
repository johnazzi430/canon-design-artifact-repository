<template>
  <div class="">
      <div class="test-header">
          Selection:
          <span id="selectedRows"></span>
      </div>
      <ag-grid-vue  class="ag-theme-balham"
                   :columnDefs="columnDefs"
                   :rowData="rowData"
                   :modules="modules">
      </ag-grid-vue>
    </div>
</template>

<script>
/*eslint-disable */
  import {AgGridVue} from "ag-grid-vue";
  import {AllCommunityModules} from '@ag-grid-community/all-modules';


  export default {
    name: 'App',
    components: {
      "ag-grid-vue": AgGridVue
    },
    data: function() {
      return {
        gridOptions: null,
        gridApi: null,
        columnApi: null,
        columnDefs: null,
        rowSelection: null,
        modules: AllCommunityModules,
        rowData: null
      };
    },
    beforeMount() {
      this.gridOptions = {};
      this.columnDefs = [
            {headerName: "Name", field: "name"},
            {headerName: "Title", field: "title"},
            {headerName: "Quote", field: "quote"},
            {headerName: "Function", field: "function"},
            {headerName: "Qty", field: "qty"},
            {headerName: "Internal or External", field: "External"}
          ];
      this.rowSelection = "single";
    },
    mounted() {
      this.gridApi = this.gridOptions.api;
      this.gridColumnApi = this.gridOptions.columnApi;
    },
    methods: {
      onSelectionChanged() {
        var selectedRows = this.gridApi.getSelectedRows();
        var selectedRowsString = "";
        selectedRows.forEach(function(selectedRow, index) {
          if (index !== 0) {
            selectedRowsString += ", ";
          }
          selectedRowsString += selectedRow.athlete;
        });
        document.querySelector("#selectedRows").innerHTML = selectedRowsString;
      },

        loadRowData() {
              fetch('/api/persona_table')
                  .then((response) => {
                      return response.json()
                  })
                  .then((json) => {
                      this.rowData = json;
                  });
          }

      },
      onGridReady(params) {
          const httpRequest = new XMLHttpRequest();
          const updateData = data => {
            this.rowData = data;
          };

          httpRequest.open(  "GET",  "/api/persona_table"  );
          httpRequest.send();
          httpRequest.onreadystatechange = () => {
            if (httpRequest.readyState === 4 && httpRequest.status === 200) {
              updateData(JSON.parse(httpRequest.responseText));
            }
          };
        },
      created() {
        this.gridOptions = {};
        this.gridOptions.columnDefs = this.createColDefs();
        this.loadRowData();
      },
  };

</script>


///

  ///////////////////////////////////////////////////////////////////

  // var gridOptions = {
  //   columnDefs: columnDefs,
  //   rowSelection: 'single',
  //   onSelectionChanged: onSelectionChanged
  // };
  //
  // var eGridDiv = document.querySelector('#myGrid');
  // new agGrid.Grid(eGridDiv, gridOptions);
  //
  //
  // function onSelectionChanged() {
  //     var selectedRows = gridOptions.api.getSelectedRows();
  //     var selectedRowsString = '';
  //     selectedRows.forEach( function(selectedRow, index) {
  //         if (index>5) {
  //             return;
  //         }
  //         if (index!==0) {
  //             selectedRowsString += ',';
  //         }
  //         selectedRowsString += selectedRow.id;
  //     });
  //
  //     // if (selectedRows.length>=5) {
  //     //     selectedRowsString += (' - and ' + (selectedRows.length - 5) + ' others');
  //     // }
  //
  //     document.querySelector('#selectedRows').innerHTML = selectedRowsString;
  //     document.getElementById("detailPanel").style.width = "500px";
  //
  //
  //     var xhttp = new XMLHttpRequest();
  //     xhttp.onreadystatechange = function() {
  //       if (this.readyState == 4 && this.status == 200) {
  //         document.getElementById("detailPanelContent").innerHTML = this.responseText;
  //       }
  //     };
  //     xhttp.open("GET", "localhost:5000/persona_table/" + selectedRowsString, true);
  //     xhttp.send();
  // }
  //

  // function closeDetail() {
  //   document.getElementById("detailPanel").style.width = "0";
  // }

  // document.addEventListener('DOMContentLoaded', function() {
  //   agGrid.simpleHttpRequest({url: '/persona_table'}).then(function(data) {
  //     gridOptions.api.setRowData(data);
  //   });
  // });
