package iit.qualitrack.frontend.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.Shapes
import androidx.compose.runtime.Composable

private val LightColors = lightColorScheme(
    primary = Primary,
    secondary = Secondary,
    primaryContainer = PrimaryVariant,
    /* you can configure other color roles here if desired */
)

@Composable
fun GarmentInspectionAppTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColors, typography = AppTypography, shapes = Shapes(), content = content
    )
}
