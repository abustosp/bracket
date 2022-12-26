import { Grid, Tooltip, createStyles, useMantineTheme } from '@mantine/core';

import { MatchInterface } from '../../interfaces/match';

const useStyles = createStyles((theme) => ({
  root: {
    width: '100%',
    marginTop: '20px',
  },
  divider: {
    backgroundColor: 'darkgray',
    height: '1px',
  },
  top: {
    // subscribe to color scheme changes right in your styles
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[2],
    paddingLeft: '15px',
    paddingTop: '6px',
    paddingBottom: '6px',
    borderRadius: '8px 8px 0px 0px',
  },
  bottom: {
    // subscribe to color scheme changes right in your styles
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[2],
    paddingLeft: '15px',
    paddingTop: '6px',
    paddingBottom: '6px',
    borderRadius: '0px 0px 8px 8px',
  },
}));

export default function Game({ match }: { match: MatchInterface }) {
  const { classes } = useStyles();
  const theme = useMantineTheme();
  const winner_style = {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.green[9] : theme.colors.green[4],
  };
  const team1_style = match.team1_score > match.team2_score ? winner_style : {};
  const team2_style = match.team1_score < match.team2_score ? winner_style : {};

  const team1_players = match.team1.players.map((player) => player.name).join(', ');
  const team2_players = match.team2.players.map((player) => player.name).join(', ');

  return (
    <div className={classes.root}>
      <div className={classes.top} style={team1_style}>
        <Tooltip label={team1_players} withArrow color="blue">
          <Grid grow>
            <Grid.Col span={10}>{match.team1.name}</Grid.Col>
            <Grid.Col span={2}>{match.team1_score}</Grid.Col>
          </Grid>
        </Tooltip>
      </div>
      <div className={classes.divider} />
      <div className={classes.bottom} style={team2_style}>
        <Tooltip label={team2_players} position="bottom" withArrow color="blue">
          <Grid grow>
            <Grid.Col span={10}>{match.team2.name}</Grid.Col>
            <Grid.Col span={2}>{match.team2_score}</Grid.Col>
          </Grid>
        </Tooltip>
      </div>
    </div>
  );
}