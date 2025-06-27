package iit.qualitrack.frontend.data.model

data class Flag(
    val id: Int,
    val operator_id: String,
    val operator_name: String?,
    val defect_type: String,
    val inspector_name: String,
    val supervisor_name: String,
    val flag_type: String,
    val issue_type: String?,
    val custom_reason: String?,
    val machine_no: String,
    val date_of_inspection: String,
    val time_of_inspection: String,
    val created_at: String
)
