package iit.qualitrack.frontend.data.model

data class InspectorDashboard(
    val total_inspections: Int,
    val total_flags: Int,
    val defect_percentage: Double,
    val red_flags: Int,
    val green_flags: Int,
    val inspector: Map<String, Any>,
    val date: String
)
