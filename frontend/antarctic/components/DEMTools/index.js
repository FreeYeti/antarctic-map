import { Component } from 'react'
import { observer, inject } from 'mobx-react'
import GeoJSON from 'ol/format/GeoJSON'

import styles from './index.less'

@inject('mapAction', 'mapStore', 'demAction', 'demStore')
@observer
class DEMTools extends Component {

    constructor(props) {
        super(props)

        this.state = {
            loading: false,
            features: null
        }
    }

    componentDidMount() {
        
    }

    handleDraw = async () => {
        let { attachDraw, exec } = this.props.demAction

        attachDraw(this.props.mapStore.map, 
            async (features) => {
                this.setState({ features: features })
                let geom = features[0].getGeometry()

                console.log(geom.getArea())


                // Convert to GeoJSON, submit to backend
                let GeoJSONHandler = new GeoJSON()
                let json = GeoJSONHandler.writeGeometry(geom)

                let result = await exec('mean', 'numpy', json)

                // alert('I am work on this feature, different approachs will take some time.')

                // Transform and show on map ?
                // console.log(geom.transform('EPSG:3031', 'EPSG:4326'))
            })
    }

    render() {
        let { enable } = this.props.demStore
        return (
            <div className={styles.demToolBox} style={{display: enable ? 'block':'none'}}>
                <div className={styles.header}>DEM Analysis</div>
                <div>
                    <span>Algorithm</span>
                    <div>
                        <input type="radio" name="algo" value="mean" defaultChecked="true" /> Mean
                        <input type="radio" name="algo" value="maximum" disabled="true" /> Maximum
                        <input type="radio" name="algo" value="minimum" disabled="true" /> Minimum
                    </div>
                    <span>Approach</span>
                    <div>
                        <input type="radio" name="approach" value="gdal" disabled="true" /> GDAL
                        <input type="radio" name="approach" value="spark" disabled="true" /> Apache Spark
                        <input type="radio" name="approach" value="numpy" defaultChecked="true" /> Numpy
                    </div>
                    <div>
                        To analyze the DEM data, please select area on the map
                        <button onClick={this.handleDraw}>Select area</button>
                    </div>
                </div>
            </div>
        )
    }
}

export default DEMTools