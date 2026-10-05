const modes = {
  idle:[0.12,0.12,0,0.1,0.6],
  exploration:[0.95,0.65,0.1,0.15,0.35],
  concentration:[0.2,0.14,0,0.95,0.68],
  conflict:[0.5,0.68,0.95,0.45,0.3],
  insight:[0.32,0.12,0,0.52,0.88],
  collapse:[0.4,0.8,0.35,0.25,0.2],
};
export const SIMULATION = Object.fromEntries(Object.entries(modes).map(([mode,v]) => [mode,{
  mode,curiosity:v[0],uncertainty:v[1],contradiction:v[2],attention:v[3],confidence:v[4],
}]));
