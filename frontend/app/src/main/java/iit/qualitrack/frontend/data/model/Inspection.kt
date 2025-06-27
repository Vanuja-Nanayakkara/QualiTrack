package iit.qualitrack.frontend.data.model

data class Inspection(
    val id: Int,
    val user: Int,
    val status: String,
    val inspection_date: String,
    val cli_inspector: Int,
    val supervisor: Int,
    val fabric_defect: Int
)
