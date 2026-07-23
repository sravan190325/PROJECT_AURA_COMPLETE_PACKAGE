const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, WidthType, BorderStyle, ShadingType, LevelFormat } = require('docx');
const fs = require('fs');

const COLORS = {
  washedBlue: "053057",
  neonTurquoise: "00EDED",
  offWhite: "F5F5F5",
};

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const heading = (text, level = 1) => {
  return new Paragraph({
    heading: level === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
    children: [new TextRun({
      text: text,
      size: level === 1 ? 32 : 28,
      color: COLORS.washedBlue,
      font: "Calibri"
    })],
    spacing: { before: level === 1 ? 240 : 180, after: 120 },
  });
};

const bodyText = (text, color = COLORS.washedBlue) => {
  return new Paragraph({
    children: [new TextRun({
      text: text,
      size: 24,
      color: color,
      font: "Calibri"
    })],
    spacing: { after: 120 }
  });
};

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Calibri", size: 24, color: COLORS.washedBlue }
      }
    }
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({
        children: [new TextRun({
          text: "STATEMENT OF WORK",
          size: 40,
          bold: true,
          color: COLORS.washedBlue,
          font: "Calibri"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 }
      }),

      new Paragraph({
        children: [new TextRun({
          text: "Enterprise Resource Planning System - Implementation & Deployment",
          size: 26,
          color: COLORS.neonTurquoise,
          font: "Calibri"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 360 }
      }),

      heading("1. EXECUTIVE SUMMARY"),
      bodyText("This Statement of Work outlines the scope, timeline, and deliverables for the implementation of a comprehensive Enterprise Resource Planning (ERP) system. The project will transform business operations across Finance, Supply Chain, Human Resources, and Manufacturing divisions."),
      bodyText("The implementation will take place over 8 months with a dedicated team of 12-15 professionals including business analysts, developers, QA engineers, and implementation specialists."),

      heading("2. PROJECT OVERVIEW"),
      heading("2.1 Project Objectives", 2),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Implement a modern, cloud-based ERP system to replace legacy systems")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Achieve 30% improvement in operational efficiency")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Enable real-time visibility across all business units")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Reduce data silos and improve decision-making capabilities")],
        spacing: { after: 240 }
      }),

      heading("2.2 Business Context", 2),
      bodyText("The organization currently operates with fragmented systems across departments, leading to data inconsistencies, manual workarounds, and delays in financial close processes. The new ERP system will create a unified platform for all business operations."),

      heading("3. SCOPE OF WORK"),
      heading("3.1 In-Scope Items", 2),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("System design and architecture")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Data migration from legacy systems")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Custom module development for HR and Supply Chain")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Integration with third-party logistics and payment systems")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("User training and change management")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Production deployment and go-live support")],
        spacing: { after: 240 }
      }),

      heading("3.2 Out-of-Scope Items", 2),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Development of mobile applications (Phase 2)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Advanced analytics and AI modules")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Hardware and infrastructure procurement")],
        spacing: { after: 360 }
      }),

      heading("4. DELIVERABLES & MILESTONES"),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2800, 3280, 3280],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                shading: { fill: COLORS.washedBlue, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Phase", bold: true, color: "FFFFFF" })],
                  alignment: AlignmentType.CENTER
                })]
              }),
              new TableCell({
                borders,
                width: { size: 3280, type: WidthType.DXA },
                shading: { fill: COLORS.washedBlue, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Key Deliverables", bold: true, color: "FFFFFF" })],
                  alignment: AlignmentType.CENTER
                })]
              }),
              new TableCell({
                borders,
                width: { size: 3280, type: WidthType.DXA },
                shading: { fill: COLORS.washedBlue, type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({
                  children: [new TextRun({ text: "Timeline", bold: true, color: "FFFFFF" })],
                  alignment: AlignmentType.CENTER
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2800, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Phase 1:\nPlanning")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Requirements documentation, System design, Risk assessment")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Month 1-2")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2800, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Phase 2:\nDevelopment")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Custom code, Integrations, Data migration scripts")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Month 3-5")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2800, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Phase 3:\nTesting")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("UAT execution, Bug fixes, Performance tuning")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Month 6-7")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 2800, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Phase 4:\nDeployment")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Go-live, Training, Production support")] }),
              new TableCell({ borders, width: { size: 3280, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph("Month 8")] })
            ]
          })
        ]
      }),

      new Paragraph({ text: "", spacing: { after: 240 } }),

      heading("5. PROJECT TIMELINE"),
      bodyText("Project Duration: 8 months (September 2025 - April 2026)"),
      bodyText("Start Date: September 1, 2025"),
      bodyText("End Date: April 30, 2026"),

      heading("6. TEAM STRUCTURE & RESOURCES"),
      bodyText("Total Team Size: 12-15 FTE (Full-Time Equivalent)"),
      bodyText("Proposed Team Composition:"),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Project Manager (1) - Overall project oversight")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Business Analysts (2) - Requirements gathering")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("System Architects (2) - System design")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Developers (5) - Custom development")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("QA Engineers (2) - Testing")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Data Specialist (1) - Data migration")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Training Specialist (1) - User training")],
        spacing: { after: 240 }
      }),

      heading("7. BUDGET & INVESTMENT"),
      bodyText("Estimated Total Project Cost: $1,200,000 - $1,500,000 USD"),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Professional Services: $800,000 - $950,000")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Software Licenses (Year 1): $250,000 - $350,000")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Training & Change Management: $75,000 - $100,000")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Infrastructure & Cloud Services: $75,000 - $100,000")],
        spacing: { after: 240 }
      }),

      heading("8. IDENTIFIED RISKS"),
      bodyText("Risk 1: Data Quality Issues - Probability: Medium | Impact: High"),
      bodyText("Mitigation: Comprehensive data audit; cleansing scripts developed early"),
      new Paragraph({ text: "", spacing: { after: 120 } }),

      bodyText("Risk 2: Resource Availability - Probability: Medium | Impact: Medium"),
      bodyText("Mitigation: Identify backup resources; flexible staffing"),
      new Paragraph({ text: "", spacing: { after: 120 } }),

      bodyText("Risk 3: Integration Complexity - Probability: High | Impact: High"),
      bodyText("Mitigation: Early integration testing; vendor involvement; POC phase"),
      new Paragraph({ text: "", spacing: { after: 240 } }),

      heading("9. DEPENDENCIES & ASSUMPTIONS"),
      heading("9.1 Critical Dependencies", 2),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Timely business stakeholder involvement")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Access to legacy system data")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Third-party vendor API availability")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Cloud infrastructure provisioning")],
        spacing: { after: 240 }
      }),

      heading("9.2 Key Assumptions", 2),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Business requirements remain stable")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Budget availability")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Consistent resource allocation")],
        spacing: { after: 360 }
      }),

      heading("10. APPROVAL & SIGN-OFF"),
      new Paragraph({ text: "", spacing: { after: 240 } }),
      bodyText("Project Sponsor: _________________________     Date: __________"),
      new Paragraph({ text: "", spacing: { after: 240 } }),
      bodyText("Project Manager: _________________________     Date: __________"),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("SOW_ERP_Implementation.docx", buffer);
  console.log("Document created successfully!");
});
