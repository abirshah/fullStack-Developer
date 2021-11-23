import React from 'react';
import {Typography, AppBar, Button, Card, CardActions, IconButton, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import VolumeDownIcon from '@mui/icons-material/VolumeDown';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import Stack from '@mui/material/Stack';
import Fingerprint from '@mui/icons-material/Fingerprint';

const App = () => {
    return (
        <div>
            <AppBar position="fixed" color={"default"}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        🐶 Pet Door System
                    </Typography>
                    <Button color="inherit">🎥 Live Feed</Button>
                    <Button color="inherit">💾 Saved Events</Button>
                </Toolbar>
            </AppBar>
            <main>
                <Container sx={{ marginTop: "10vh" }}>
                    <Grid container spacing={2}>
                        <Grid item xs={8}>
                            <Card >
                                <CardMedia
                                    component="img"
                                    image="http://localhost:5000/video"
                                    alt="green iguana"
                                />
                                <CardContent>
                                    <Typography gutterBottom variant="h5" component="div">
                                        Live Video Feed
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                </CardActions>
                            </Card>
                        </Grid>
                        <Grid item xs={4}>
                            <Card>
                                <CardContent>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                        Door Status
                                    </Typography>
                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                                        LOCKED
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <IconButton aria-label="fingerprint" color="warning">
                                        <LockIcon />
                                    </IconButton>
                                    <IconButton aria-label="fingerprint" color="success">
                                        <LockOpenIcon />
                                    </IconButton>
                                </CardActions>
                            </Card>
                        </Grid>
                    </Grid>
                </Container>
            </main>
        </div>
    )
}

export default App;