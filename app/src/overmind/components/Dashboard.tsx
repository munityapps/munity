import './Dashboard.scss';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import iconOvmIncome from '../../assets/icon_ovm_income.svg';
import iconOvmUser from '../../assets/icon_ovm_user.svg';
import iconOvmAction from '../../assets/icon_ovm_action.svg';
import iconOvmCustomer from '../../assets/icon_ovm_customer.svg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button } from 'primereact/button';
import { useTranslation } from 'react-i18next';
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';

let category = [];
let dottedBase = +new Date();
let lineData = [];
let barData = [];

for (let i = 0; i < 20; i++) {
  let date = new Date((dottedBase += 3600 * 24 * 1000));
  category.push(
    [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-')
  );
  let b = Math.random() * 200;
  let d = Math.random() * 200;
  barData.push(b);
  lineData.push(d + b);
}

// options
const option1 = {
  backgroundColor: '#0f375f',
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    data: ['line', 'bar'],
    textStyle: {
      color: '#ccc'
    }
  },
  xAxis: {
    data: category,
    axisLine: {
      lineStyle: {
        color: '#ccc'
      }
    }
  },
  yAxis: {
    splitLine: { show: false },
    axisLine: {
      lineStyle: {
        color: '#ccc'
      }
    }
  },
  series: [
    {
      name: 'line',
      type: 'line',
      smooth: true,
      showAllSymbol: true,
      symbol: 'emptyCircle',
      symbolSize: 15,
      data: lineData
    },
    {
      name: 'bar',
      type: 'bar',
      barWidth: 10,
      itemStyle: {
        borderRadius: 5,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#14c8d4' },
          { offset: 1, color: '#43eec6' }
        ])
      },
      data: barData
    },
    {
      name: 'line',
      type: 'bar',
      barGap: '-100%',
      barWidth: 10,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(20,200,212,0.5)' },
          { offset: 0.2, color: 'rgba(20,200,212,0.2)' },
          { offset: 1, color: 'rgba(20,200,212,0)' }
        ])
      },
      z: -12,
      data: lineData
    },
    {
      name: 'dotted',
      type: 'pictorialBar',
      symbol: 'rect',
      itemStyle: {
        color: '#0f375f'
      },
      symbolRepeat: true,
      symbolSize: [12, 4],
      symbolMargin: 1,
      z: -10,
      data: lineData
    }
  ]
};

// option2
const option2 = {
  backgroundColor: '#2c343c',
  title: {
    text: 'Main clients in actions by day',
    left: 'center',
    top: 20,
    textStyle: {
      color: '#ccc'
    }
  },
  tooltip: {
    trigger: 'item'
  },
  visualMap: {
    show: false,
    min: 80,
    max: 600,
    inRange: {
      colorLightness: [0, 1]
    }
  },
  series: [
    {
      name: 'More active clients',
      type: 'pie',
      radius: '55%',
      center: ['25%', '50%'],
      data: [
        { value: 335, name: 'Nice client' },
        { value: 100, name: 'Lazy client' },
        { value: 274, name: 'Main client 2' },
        { value: 235, name: 'Main client 1' },
        { value: 400, name: 'Demo' }
      ].sort(function (a, b) {
        return a.value - b.value;
      }),
      roseType: 'radius',
      label: {
        color: 'rgba(255, 255, 255, 0.3)'
      },
      labelLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        },
        smooth: 0.2,
        length: 10,
        length2: 20
      },
      itemStyle: {
        color: '#c23531',
        shadowBlur: 200,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      },
      animationType: 'scale',
      animationEasing: 'elasticOut',
      animationDelay: function () {
        return Math.random() * 200;
      }
    },
    {
      name: 'More active clients',
      type: 'pie',
      radius: '55%',
      center: ['75%', '50%'],
      data: [
        { value: 335, name: 'Nice client' },
        { value: 100, name: 'Lazy client' },
        { value: 274, name: 'Main client 2' },
        { value: 235, name: 'Main client 1' },
        { value: 400, name: 'Demo' }
      ].sort(function (a, b) {
        return a.value - b.value;
      }),
      roseType: 'radius',
      label: {
        color: 'rgba(255, 255, 255, 0.3)'
      },
      labelLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        },
        smooth: 0.2,
        length: 10,
        length2: 20
      },
      itemStyle: {
        color: '#c23531',
        shadowBlur: 200,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      },
      animationType: 'scale',
      animationEasing: 'elasticOut',
      animationDelay: function () {
        return Math.random() * 200;
      }
    }
  ]
};


const Dashboard = () => {
    const { t } = useTranslation();
    return <div className="dashboard">
        <div style={{marginTop:0, marginBottom:'20px', color:'#FFFFFF !important'}} className="income-graph p-shadow-4 p-jc-between p-d-flex p-ai-center">
            <div className="title" style={{color:'white'}}>
                &nbsp; Dashboard for my platform
            </div>
        </div>
        <div className="metrics">
            <div className="metric p-shadow-4">
                <img src={iconOvmIncome} alt="iconme" />
                <div className="desc">
                    <div className="legend">Income on last 29 days</div>
                    <div className="count">1,2M€</div>
                </div>
            </div>
            <div className="metric p-shadow-4">
                <img src={iconOvmCustomer} alt="" />
                <div className="desc">
                    <div className="legend">Total user on all platform</div>
                    <div className="count">900</div>
                </div>
            </div>
            <div className="metric p-shadow-4">
                <img src={iconOvmAction} alt="" />
                <div className="desc">
                    <div className="legend">Average actions by day</div>
                    <div className="count">35,000</div>
                </div>
            </div>
            <div className="metric p-shadow-4">
                <img src={iconOvmUser} alt="" />
                <div className="desc">
                    <div className="legend">Current active clients</div>
                    <div className="count">127</div>
                </div>
            </div>
        </div>
        <div className="income-graph p-shadow-4">
            <div className="title">
                Income for next 2 weeks
            </div>
            <ReactECharts className="graph1" option={option1} />
        </div>
        <div className="income-graph p-shadow-4">
            <div className="title">
                Mainly active clients
            </div>
            <ReactECharts className="graph2" option={option2} />
        </div>
    </div >;
};

export default Dashboard;
