# Transient effects

## Reduction of usable heat during start-up of each component

![Heat reduction during start-up](fig/221028_Start-up-Reduction_general.svg)

Linear warm-up during start-up:
$$
 \dot{Q}_{out,reduced} = 
\begin{cases}
\dot{Q}_{out} \ \frac{\text{actual operating time}}{\text{start-up time}} & \text{actual operating time} \ < \text{start-up time} \\
\dot{Q}_{out} & \text{actual operating time} \ \geq  \text{start-up time}
\end{cases} 
$$