import React, { useState, useEffect } from 'react';
import {
    Typography,
    AppBar,
    Button,
    Card,
    Chip,
    CardActions,
    IconButton,
    CardContent,
    CardMedia,
    CssBaseline,
    Grid,
    Toolbar,
    Container,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper
} from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import DoorBackTwoToneIcon from '@mui/icons-material/DoorBackTwoTone';
import PlayCircleFilledTwoToneIcon from '@mui/icons-material/PlayCircleFilledTwoTone';
import { useTheme, ThemeProvider, createTheme } from '@mui/material/styles';
import {getEvents} from './services/events'

function createData(start, objects, access, video) {
    return { start, objects, access, video };
}

const rows = [
    createData('Tue Nov 23, 6:43 PM', "Cat, Dog, Package", false, 'https://miro.medium.com/max/1200/1*pyDWEf7qautBRq3lcw5xew.gif'),
    createData('Tue Nov 23, 6:43 PM', "Cat, Dog, Package", false, 'https://miro.medium.com/max/1200/1*pyDWEf7qautBRq3lcw5xew.gif'),
    createData('Tue Nov 23, 6:43 PM', "Cat, Dog, Package", false, 'https://miro.medium.com/max/1200/1*pyDWEf7qautBRq3lcw5xew.gif'),
    createData('Tue Nov 23, 6:43 PM', "Cat, Dog, Package", false, 'https://miro.medium.com/max/1200/1*pyDWEf7qautBRq3lcw5xew.gif'),
    createData('Tue Nov 23, 6:43 PM', "Cat, Dog, Package", false, 'https://miro.medium.com/max/1200/1*pyDWEf7qautBRq3lcw5xew.gif')
];

const  App = () => {
    const theme = createTheme({
        palette: {
            mode: 'dark',
        },
    });
    const LIVE_STREAM_URL = "http://127.0.0.1:5000/video";
    const [videoSource, setVideoSource] = useState(LIVE_STREAM_URL);
    const [watchingStream, setWatchingStream] = useState(true);
    const [events, setEvents] = useState([]);

    useEffect(() => {
        let mounted = true;
        getEvents()
            .then(items => {
                if(mounted) {
                    setEvents(items)
                }
            })
        return () => mounted = false;
    }, [])

    const watchSavedEvent = (e) => {
        let url ='https://video-snapshots.s3.amazonaws.com/' + e.currentTarget.value;
        console.log(url)
        setVideoSource(url);
        setWatchingStream(false)
    }

    const watchStream = () => {
        setVideoSource('http://localhost:5000/video');
        setWatchingStream(true)
    }

    return (
        <ThemeProvider theme={theme} >
            <CssBaseline />
            <AppBar position="fixed" color={"default"} sx={{ height: "8vh" }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        🐶 Pet Door System
                    </Typography>
                    <Button color="inherit">🎥 Video</Button>
                    <Button color="inherit">💾 Events</Button>
                    <Button color="inherit">⚙️ Settings</Button>
                </Toolbar>
            </AppBar>
            <main>
                <Container sx={{ marginTop: "10vh" }}>
                    <Grid container spacing={2}>
                        <Grid item sm={6} xs={12}>
                            <Card >
                                <CardMedia
                                    component="img"
                                    image={videoSource}
                                    alt="green iguana"
                                />
                                <CardContent>
                                    <Typography gutterBottom variant="h5" component="div">
                                        Live Video Feed
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    {!watchingStream &&
                                    <Button size={"small"} onClick={watchStream} variant="outlined" startIcon={<PlayCircleFilledTwoToneIcon />}>
                                        Back to Camera Feed
                                    </Button>
                                    }
                                </CardActions>
                            </Card>
                        </Grid>
                        <Grid item sm={3} xs={6}>
                            <Card>
                                <CardContent sx={{height: "12vh"}}>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                        Pet Door Status
                                    </Typography>
                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                                        <Chip icon={<DoorBackTwoToneIcon />} color="error" label="Locked" />
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <Button size={"medium"}>Access History</Button>
                                </CardActions>
                            </Card>
                        </Grid>
                        <Grid item sm={3} xs={6}>
                            <Card>
                                <CardContent sx={{height: "12vh"}}>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                        Remote Override
                                    </Typography>
                                    <Typography sx={{ mb: 1.5 }} color="text.secondary">

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
                        <Grid item sm={12} xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                                        Events
                                    </Typography>
                                    <TableContainer component={Paper}>
                                        <Table sx={{ minWidth: 650 }} aria-label="simple table">
                                            <TableHead>
                                                <TableRow>
                                                    <TableCell>Event Start</TableCell>
                                                    <TableCell >Objects Detected</TableCell>
                                                    <TableCell>Access Granted</TableCell>
                                                    <TableCell >Event Clip</TableCell>
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {events.map((row) => (
                                                    <TableRow
                                                        key={row.name}
                                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                                    >
                                                        <TableCell component="th" scope="row">
                                                            {row.ts}
                                                        </TableCell>
                                                        <TableCell >{row.classes}</TableCell>
                                                        <TableCell >{row.access_granted.toString()}</TableCell>
                                                        <TableCell >
                                                            <Button size={"small"} value={row.video} href={'https://video-snapshots.s3.amazonaws.com/' + row.video} variant="outlined" startIcon={<PlayCircleFilledTwoToneIcon />} download>
                                                                Download Clip
                                                            </Button>
                                                        </TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </TableContainer>
                                </CardContent>
                                <CardActions>
                                </CardActions>
                            </Card>
                        </Grid>
                    </Grid>
                </Container>
            </main>
        </ThemeProvider>
    )
}

export default App;