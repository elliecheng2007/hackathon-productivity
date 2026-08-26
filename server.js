const express = require('express');
const app = express();

// Parses incoming JSON payloads from GitHub
app.use(express.json());

// In-memory database
const teams = {};

// 1. Webhook Endpoint (GitHub pushes data here)
app.post('/api/github-webhook', (req, res) => {
  const teamId = req.query.teamId;
  if (!teamId) return res.status(400).send('Missing teamId parameter');

  // Initialize team if new
  if (!teams[teamId]) {
    teams[teamId] = { gitCommits: 0, cappedLines: 0 };
  }

  const commits = req.body.commits || [];
  if (commits.length === 0) return res.status(200).send('No commits');

  let rawLines = 0;
  commits.forEach(c => {
    rawLines += (c.added ? c.added.length * 10 : 0) + (c.modified ? c.modified.length * 5 : 0);
  });

  teams[teamId].gitCommits += commits.length;
  teams[teamId].cappedLines += Math.min(300, rawLines);

  console.log(`[Git Push] ${teamId}: +${commits.length} commits`);
  res.status(200).send('OK');
});

// 2. Leaderboard Endpoint (Teammate fetches this)
app.get('/api/leaderboard', (req, res) => {
  const leaderboard = Object.keys(teams).map(teamId => {
    const data = teams[teamId];
    const score = Math.min(100, (data.gitCommits * 1000) + Math.round(data.cappedLines * 1));

    return {
      teamId,
      gitCommits: data.gitCommits,
      cappedLines: data.cappedLines,
      score: score
    };
  });

  leaderboard.sort((a, b) => b.score - a.score);
  res.json(leaderboard);
});

// Start the server on port 3000
app.listen(3000, () => console.log('Express server running on http://localhost:3000'));

