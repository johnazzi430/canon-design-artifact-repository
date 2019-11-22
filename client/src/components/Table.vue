<template>
    <div>
      <div class="test-header">
            Selection:
              <span id="selectedRows"></span>
      </div>
      <ag-grid-vue style="width: 100%; height: 500px;"
                   class="ag-theme-balham"
                   :columnDefs="columnDefs"
                   :rowData="rowData"
                   :modules="modules"
                   rowSelection="single"
                   @grid-ready="onGridReady"
                   @selection-changed="onSelectionChanged">
      </ag-grid-vue>
    </div>
</template>

<script>
/*eslint-disable */
    import {AgGridVue} from "@ag-grid-community/vue";
    import {AllCommunityModules} from '@ag-grid-community/all-modules';
    export default {
        name: 'App',
        data() {
            return {
                columnDefs: null,
                rowData: null,
                rowSelection: null,
                gridApi: null,
                gridOptions: null,
                modules: AllCommunityModules
            }
        },
        components: {
            AgGridVue
        },
        methods: {
                    onGridReady(params) {
                        this.gridApi = params.api;
                        this.columnApi = params.columnApi;
                    },
                    onSelectionChanged() {
                          var selectedRows = this.gridApi.getSelectedRows();
                          var selectedRowsString = "";
                          selectedRows.forEach(function(selectedRow, index) {
                            if (index !== 0) {
                              selectedRowsString += ", ";
                            }
                            selectedRowsString += selectedRow.name;
                          });
                          document.querySelector("#selectedRows").innerHTML = selectedRowsString;
                        },
                },
        beforeMount() {
          this.columnDefs = [
            {headerName: "Name", field: "name"},
            {headerName: "Title", field: "title"},
            {headerName: "Quote", field: "quote"},
            {headerName: "Function", field: "function"},
            {headerName: "Qty", field: "qty"},
            {headerName: "Internal or External", field: "External"}
          ];
          this.rowSelection = "single";
          fetch('http://localhost:5000/api/persona-table')
                          .then(result => result.json())
                          .then(rowData => this.rowData = rowData);
        },
    }
</script>

<style>
</style>
