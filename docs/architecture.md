
# RetailPulse — System Architecture

## 1. Architecture Overview

RetailPulse is an end-to-end retail analytics platform that transforms raw transaction data into business intelligence.

```drawio
<mxfile>
  <diagram id="HFSCROB18h9VKuq_ITEd" name="Page-1">
    <mxGraphModel dx="1524" dy="1479" grid="1" gridSize="10" guides="1" tooltips="0" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="ihLqYF2HSY6j2O4yohCy-0" />
        <mxCell id="ihLqYF2HSY6j2O4yohCy-1" parent="ihLqYF2HSY6j2O4yohCy-0" />
        <UserObject label="" mermaidData="{&#xa;  &quot;data&quot;: &quot;flowchart TD\r\n    A[\&quot;UCI Online Retail Dataset&lt;br/&gt;Excel File\&quot;] --&gt; B[\&quot;Data Ingestion&lt;br/&gt;Python\&quot;]\r\n    B --&gt; C[\&quot;Data Cleaning&lt;br/&gt;Pandas and NumPy\&quot;]\r\n    C --&gt; D[\&quot;Transaction Classification\&quot;]\r\n\r\n    D --&gt; E[\&quot;Clean Sales\&quot;]\r\n    D --&gt; F[\&quot;Returns\&quot;]\r\n    D --&gt; G[\&quot;Cancelled Transactions\&quot;]\r\n    D --&gt; H[\&quot;Rejected Records\&quot;]\r\n\r\n    E --&gt; I[\&quot;ETL Validation&lt;br/&gt;Reconciliation\&quot;]\r\n    F --&gt; I\r\n    G --&gt; I\r\n    H --&gt; I\r\n\r\n    I --&gt; J[\&quot;MySQL Database\&quot;]\r\n    J --&gt; K[\&quot;SQL Business Analysis\&quot;]\r\n    K --&gt; L[\&quot;Power BI Dashboard\&quot;]\r\n\r\n    M[\&quot;Pipeline Orchestration&lt;br/&gt;Python\&quot;] -.-&gt; B\r\n    M -.-&gt; C\r\n    M -.-&gt; I\r\n    M -.-&gt; J\r\n\r\n    N[\&quot;Logging and Reports\&quot;] -.-&gt; M\r\n    O[\&quot;Automated Tests&lt;br/&gt;Pytest\&quot;] -.-&gt; M&quot;,&#xa;  &quot;config&quot;: null&#xa;}" id="5QynSo0e4J83fQaPfeq1-0">
          <mxCell connectable="0" parent="ihLqYF2HSY6j2O4yohCy-1" style="group;transparentBounds=1;editIcon=1;lockedGroup=0;groupPadding=10;" vertex="1">
            <mxGeometry as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="UCI Online Retail Dataset&#xa;Excel File" mermaidId="n:A" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="UCI Online Retail Dataset&#xa;Excel File" id="ihLqYF2HSY6j2O4yohCy-2">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="241" x="145" y="133" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Data Ingestion&#xa;Python" mermaidId="n:B" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Data Ingestion&#xa;Python" id="ihLqYF2HSY6j2O4yohCy-3">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="162" x="195" y="256" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Data Cleaning&#xa;Pandas and NumPy" mermaidId="n:C" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Data Cleaning&#xa;Pandas and NumPy" id="ihLqYF2HSY6j2O4yohCy-4">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="194" x="237" y="379" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Transaction Classification" mermaidId="n:D" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Transaction Classification" id="ihLqYF2HSY6j2O4yohCy-5">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="242" x="213" y="502" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Clean Sales" mermaidId="n:E" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Clean Sales" id="ihLqYF2HSY6j2O4yohCy-6">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="141" x="10" y="606" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Returns" mermaidId="n:F" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Returns" id="ihLqYF2HSY6j2O4yohCy-7">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="114" x="201" y="606" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Cancelled Transactions" mermaidId="n:G" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Cancelled Transactions" id="ihLqYF2HSY6j2O4yohCy-8">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="223" x="365" y="606" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rejected Records" mermaidId="n:H" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rejected Records" id="ihLqYF2HSY6j2O4yohCy-9">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="184" x="638" y="606" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="ETL Validation&#xa;Reconciliation" mermaidId="n:I" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="ETL Validation&#xa;Reconciliation" id="ihLqYF2HSY6j2O4yohCy-10">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="162" x="396" y="710" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="MySQL Database" mermaidId="n:J" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="MySQL Database" id="ihLqYF2HSY6j2O4yohCy-11">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="176" x="603" y="833" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="SQL Business Analysis" mermaidId="n:K" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="SQL Business Analysis" id="ihLqYF2HSY6j2O4yohCy-12">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="211" x="586" y="937" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Power BI Dashboard" mermaidId="n:L" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Power BI Dashboard" id="ihLqYF2HSY6j2O4yohCy-13">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="201" x="591" y="1041" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Pipeline Orchestration&#xa;Python" mermaidId="n:M" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Pipeline Orchestration&#xa;Python" id="ihLqYF2HSY6j2O4yohCy-14">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="220" x="554" y="133" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Logging and Reports" mermaidId="n:N" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Logging and Reports" id="ihLqYF2HSY6j2O4yohCy-15">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="204" x="442" y="20" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Automated Tests&#xa;Pytest" mermaidId="n:O" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Automated Tests&#xa;Pytest" id="ihLqYF2HSY6j2O4yohCy-16">
          <mxCell parent="5QynSo0e4J83fQaPfeq1-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="179" x="696" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:A-&gt;B#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.46;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-17">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-2" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.46;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="266" y="231" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:B-&gt;C#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.32;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-18">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-3" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.32;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="276" y="354" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:C-&gt;D#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-19">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-4" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:D-&gt;E#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-20">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="81" y="581" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:D-&gt;F#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.33;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-21">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.33;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="258" y="581" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:D-&gt;G#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.81;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-22">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.81;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="477" y="581" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:D-&gt;H#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.8;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-23">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.8;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-9">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="730" y="581" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:E-&gt;I#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.33;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-24">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-6" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.33;" target="ihLqYF2HSY6j2O4yohCy-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="81" y="685" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:F-&gt;I#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.19;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-25">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-7" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.19;" target="ihLqYF2HSY6j2O4yohCy-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="258" y="685" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:G-&gt;I#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-26">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-8" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:H-&gt;I#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=1;entryY=0.23;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-27">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-9" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=1;entryY=0.23;" target="ihLqYF2HSY6j2O4yohCy-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="730" y="685" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:I-&gt;J#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.11;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-28">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-10" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.11;" target="ihLqYF2HSY6j2O4yohCy-11">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="477" y="808" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:J-&gt;K#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-29">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-11" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-12">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:K-&gt;L#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-30">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-12" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-13">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:M-&gt;B#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.95;entryX=1;entryY=0.12;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-31">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-14" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.95;entryX=1;entryY=0.12;" target="ihLqYF2HSY6j2O4yohCy-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="454" y="231" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:M-&gt;C#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.42;exitY=1;entryX=1;entryY=0.23;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-32">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-14" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.42;exitY=1;entryX=1;entryY=0.23;" target="ihLqYF2HSY6j2O4yohCy-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="634" y="231" />
                <mxPoint x="634" y="293" />
                <mxPoint x="634" y="354" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:M-&gt;I#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.95;entryX=1;entryY=0.33;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-33">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-14" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.95;entryX=1;entryY=0.33;" target="ihLqYF2HSY6j2O4yohCy-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="872" y="231" />
                <mxPoint x="872" y="293" />
                <mxPoint x="872" y="354" />
                <mxPoint x="872" y="416" />
                <mxPoint x="872" y="477" />
                <mxPoint x="872" y="529" />
                <mxPoint x="872" y="581" />
                <mxPoint x="872" y="633" />
                <mxPoint x="872" y="685" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:M-&gt;J#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.9;entryX=1;entryY=0.07;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-34">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-14" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.9;entryX=1;entryY=0.07;" target="ihLqYF2HSY6j2O4yohCy-11">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="892" y="231" />
                <mxPoint x="892" y="293" />
                <mxPoint x="892" y="354" />
                <mxPoint x="892" y="416" />
                <mxPoint x="892" y="477" />
                <mxPoint x="892" y="529" />
                <mxPoint x="892" y="581" />
                <mxPoint x="892" y="633" />
                <mxPoint x="892" y="685" />
                <mxPoint x="892" y="747" />
                <mxPoint x="892" y="808" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:N-&gt;M#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.18;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-35">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-15" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.18;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-14">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="544" y="108" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:O-&gt;M#0" mermaidBaseStyle="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.83;entryY=0;" mermaidBaseValue="" id="ihLqYF2HSY6j2O4yohCy-36">
          <mxCell edge="1" parent="5QynSo0e4J83fQaPfeq1-0" source="ihLqYF2HSY6j2O4yohCy-16" style="curved=1;dashed=1;dashPattern=2 3;fixDash=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.83;entryY=0;" target="ihLqYF2HSY6j2O4yohCy-14">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="785" y="108" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

```

## 2. Technology Architecture

| Layer | Technology |
|---|---|
| Source | Excel, UCI Online Retail |
| Ingestion | Python |
| Processing | Pandas, NumPy |
| Validation | Python |
| Storage | MySQL |
| Analytics | SQL |
| Visualization | Power BI |
| Automation | Python |
| Testing | Pytest |
| Logging | Python Logging |

## 3. Data Flow

1. Raw Excel transactions are ingested.
2. Data is cleaned and standardized.
3. Transactions are classified into sales, returns, cancellations, and rejected records.
4. ETL validation checks the generated outputs.
5. Validated datasets are loaded into MySQL.
6. SQL queries perform business analysis.
7. Power BI presents the analytical results.

## 4. Quality Assurance

- Duplicate record detection
- Missing-value handling
- Transaction classification
- ETL reconciliation
- Database row-count verification
- Automated unit tests
- Pipeline execution logs

## 5. Execution

Run the complete pipeline:

```powershell
python -m src.automation.run_pipeline
```

Run automated tests:

```powershell
python -m pytest tests/ -v
```
